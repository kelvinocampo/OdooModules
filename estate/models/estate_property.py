from odoo import api, models, fields
from odoo.exceptions import UserError

class Property(models.Model):
    _name = "estate.property"
    _description = "Properties "

    name = fields.Char(
        string='Nombre de la Propiedad',
        required=True,
        index=True,
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
        required=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        help='Fecha cuando la propiedad estará disponible'
    )
    expected_price = fields.Float(
        string='Precio Esperado',
        digits='Product Price',
        required=True
    )
    selling_price = fields.Float(
        string='Precio de Venta',
        digits='Product Price',
        readonly=True,
        copy=False
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
    property_type_id= fields.Many2one("estate.property.type", string="Type")
    buyer = fields.Many2one('res.partner', string='Buyer', index=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string='Tags')
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offer')
    total_area = fields.Float(compute="_compute_total_area", string="Total Area", store=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", store=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >=0)', 'The expected price must a positive number.'),
        ('check_selling_price', 'CHECK(selling_price >=0 OR selling_price=null)', 'The selling price must a positive number.'),
    ]
    
    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            except ValueError:
                record.best_price = 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area=10
                record.garden_orientation="North"
            else:
                record.garden_area=0
                record.garden_orientation=False

    def action_cancel_property(self):
        for record in self:
            if record.state == 'Sold':
                raise UserError('A Sold property can not be canceled.')
        return self.write({'state': 'Cancelled'})
    
    def action_sold_property(self):
        for record in self:
            if record.state == 'Cancelled':
                raise UserError('No puedes vender una propiedad cancelada')
            if not any(offer.status == 'Accepted' for offer in record.offer_ids):
                raise UserError('Debes aceptar una oferta antes de marcar como vendida')
        return self.write({'state': 'Sold'})
    
    @api.ondelete(at_uninstall=False)
    def _check_property_state_before_delete(self):
        for prop in self:
            if prop.state not in ('new', 'cancelled'):
                raise UserError('You cannot delete a property that is not in "New" or "Cancelled" state.')