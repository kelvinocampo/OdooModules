from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Properties"
    _order="name"

    name = fields.Char(
        string='Nombre del Tipo de la Propiedad',
        required=True,
        index=True,
        help='Nombre del tipo de la propiedad inmobiliaria'
    )
    property_ids = fields.One2many("estate.property","property_type_id", string="Property")
    sequence = fields.Integer(
        string='Sequence',
        default=1,
        help="Used to order types. Lower is better."
    )

    _sql_constraints = [
        ('check_name', 'unique(name)', 'The type must be unique.')
    ]
