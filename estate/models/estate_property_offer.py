from odoo import models, fields

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Properties "

    price = fields.Float(
        string='Precio',
        digits='Price'
    )

    status = fields.Selection(
        string='Orientación del Jardín',
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        copy=False,
        help='Orientación cardinal principal del jardín'
    )
    
    property_id = fields.Many2one('estate.property', string='Property', index=True, required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required=True)