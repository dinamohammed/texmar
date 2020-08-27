# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SOLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    to_sell = fields.Boolean("Sell")
    
    to_request = fields.Boolean("Request")
    
    custom_model_id = fields.Many2one('so.lines', 'Custom Model')

    

class SOInherit(models.Model):
    _inherit = 'sale.order'
    
    def prepare_sol(self):
        sol ={}
        
        self.ensure_one()
            
        for record in self:
            for line in record.order_line:
                if line.to_sell:
                    sol = {'product_id' : line.product_id.id,
                            'name' : line.name,
                            'product_uom_qty' : line.product_uom_qty,
                            'price_unit' : line.price_unit,
                            'price_subtotal' : line.price_subtotal}
                    
        raise ValidationError(sol['name'])
        return sol
                
                
      
