# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SOLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    to_sell = fields.Boolean("Sell")
    
    to_request = fields.Boolean("Request")
    
    custom_model_id = fields.Many2one('so.lines', 'Custom Model')

    

class SOInherit(models.Model):
    _inherit = 'sale.order'
    
    def _prepare_sol(self):
         self .ensure_one()
         if self.to_sale :
            return { 'name' : self.name,
                    'product_id' : self.product_id.id, 
                    'product_uom_id' : self.product_uom_id}