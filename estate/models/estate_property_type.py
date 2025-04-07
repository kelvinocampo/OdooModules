from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Properties"

    name = fields.Char(
        string='Nombre del Tipo de la Propiedad',
        required=True,
        index=True,
        help='Nombre del tipo de la propiedad inmobiliaria'
    )

    _sql_constraints = [
        ('check_name', 'unique(name)', 'The type must be unique.')
    ]
