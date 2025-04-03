from odoo import models, fields

class Property(models.Model):
    _name = "estate.property"
    _description = "CRM Recurring revenue plans"

    name = fields.Char(
        string='Nombre de la Propiedad',
        required=True,
        index=True,
        tracking=True,
        help='Nombre oficial de la propiedad inmobiliaria'
    )

    description = fields.Text(
        string='Descripción Detallada',
        translate=True,
        help='Descripción completa de las características de la propiedad'
    )

    postcode = fields.Char(
        string='Código Postal',
        size=10,
        help='Código postal de la ubicación de la propiedad'
    )

    date_availability = fields.Date(
        string='Fecha Disponible',
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        help='Fecha cuando la propiedad estará disponible'
    )

    expected_price = fields.Float(
        string='Precio Esperado',
        digits='Product Price',
        required=True,
        tracking=True
    )

    selling_price = fields.Float(
        string='Precio de Venta',
        digits='Product Price',
        readonly=True,
        copy=False,
        tracking=True
    )

    bedrooms = fields.Integer(
        string='Habitaciones',
        default=2,
        help='Número de habitaciones en la propiedad'
    )

    living_area = fields.Integer(
        string='Área Habitable (m²)',
        help='Área total de espacio habitable en metros cuadrados'
    )

    facades = fields.Integer(
        string='Fachadas',
        help='Número de fachadas que tiene la propiedad'
    )

    garage = fields.Boolean(
        string='Garaje',
        help='Indica si la propiedad incluye garaje'
    )

    garden = fields.Boolean(
        string='Jardín',
        help='Indica si la propiedad tiene área de jardín'
    )

    garden_area = fields.Integer(
        string='Área del Jardín (m²)',
        help='Tamaño del jardín en metros cuadrados'
    )

    garden_orientation = fields.Selection(
        string='Orientación del Jardín',
        selection=[
            ('North', 'Norte'),
            ('South', 'Sur'),
            ('East', 'Este'),
            ('West', 'Oeste')
        ],
        help='Orientación cardinal principal del jardín'
    )

    active = fields.Boolean(
        default=True
    )

    state = fields.Selection(
        string='Estado',
        selection=[
            ('New', 'New'),
            ('Offer Received', 'Offer Received'),
            ('Offer Accepted', 'Offer Accepted'),
            ('Sold', 'Sold'),
            ('Cancelled', 'Cancelled')
        ],
        required=True,
        default="New",
        copy=False,
        help='Estado de la propiedad'
    )