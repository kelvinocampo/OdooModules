from odoo import models, api, fields
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

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
    property_type_id = fields.Many2one(related="property_id.property_type_id",string="Property Type", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price >=0)', 'The price must a positive number.')
    ]

    @api.constrains('price')
    def _check_price(self):
        for offer in self:
            if float_is_zero(offer.property_id.expected_price, precision_digits=2):
                continue
            min_price = offer.property_id.expected_price * 0.9
            if float_compare(offer.price, min_price, precision_digits=2) < 0:
                raise ValidationError(f"El precio de la oferta debe ser al menos 90% del precio esperado (Mínimo: {min_price})")
    
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
        for offer in self:
            if offer.property_id.state in ('Sold', 'Cancelled'):
                raise UserError("No se puede aceptar una oferta en propiedades vendidas o canceladas")
            if "Accepted" in offer.property_id.offer_ids.mapped('status'):
                raise UserError("Ya hay una oferta aceptada")
        self.write({'status': 'Accepted'})
        return self.property_id.write({
            'state': 'Offer Accepted',
            'selling_price': self.price,
            'buyer': self.partner_id.id
        })

    def action_refuse(self):
        return self.write(
            {
                "status": "Refused",
            }
        )