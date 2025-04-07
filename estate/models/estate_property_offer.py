from odoo import models, api, fields
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers Properties"
    _order = 'price desc'  # Ordenar ofertas por precio descendente

    price = fields.Float(string='Precio', digits='Price')
    status = fields.Selection(
        [('Accepted', 'Accepted'), ('Refused', 'Refused')],
        string='Estado',
        copy=False
    )
    property_id = fields.Many2one('estate.property', required=True, index=True)
    partner_id = fields.Many2one('res.partner', required=True, index=True)
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        string="Deadline"
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price >=0)', 'The price must a positive number.')
    ]

    # A Terminar
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if (100 * float(record.price)/float(record.property_id.expected_price)) < 90:
                raise ValidationError("The offer price should be atleast 90% of the expected price.")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = fields.Date.to_date(offer.create_date)
                offer.date_deadline = create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                create_date = fields.Date.to_date(offer.create_date)
                offer.validity = (offer.date_deadline - create_date).days
            elif offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        if "Accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer has already been accepted.")
        self.write(
            {
                "state": "Accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "Offer Accepted",
                "selling_price": self.price,
                "buyer": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "status": "Refused",
            }
        )