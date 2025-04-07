from odoo import models, api, fields
from datetime import timedelta

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