from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Properties"
    _order="name"

    name = fields.Char(
        string='Caracteristica de la Propiedad',
        required=True,
        index=True,
        help='Etiqueta/Caracteristica de la propiedad inmobiliaria'
    )
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('check_name', 'unique(name)', 'The tag must be unique.')
    ]
