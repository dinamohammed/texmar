# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
    
#     def action_todraft_stock(self):
#         for pick in self:
#             pick.sudo().write({'state':'draft'})
            
#             for move in pick.move_ids_without_package:
#                 move.sudo().write({'state':'draft'})
    
    
    



class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    
    def action_validate_stock(self):
        #self.env['stock.picking'].search([('origin','=',self.name)] ,limit=1).button_validate()
        self.picking_ids.button_validate()
        return True