from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Properties"

    name = fields.Char(
        string='Caracteristica de la Propiedad',
        required=True,
        index=True,
        help='Etiqueta/Caracteristica de la propiedad inmobiliaria'
    )
