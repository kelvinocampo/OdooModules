from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    def action_sold_property(self):
        super_result = super().action_sold_property()
        
        for property in self:
            if not property.buyer or not property.selling_price:
                continue  
            
            invoice_line_vals = [
                (0, 0, {
                    'name': f'Comisión por venta de {property.name}',
                    'quantity': 1,
                    'price_unit': property.selling_price * 0.06, 
                }),
                (0, 0, {
                    'name': 'Gastos administrativos',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]
            
            invoice_vals = {
                'partner_id': property.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': invoice_line_vals,
            }
            
            self.env['account.move'].create(invoice_vals)
            
        return super_result