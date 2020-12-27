# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from num2words import num2words
                                

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #Adding a Quantity Total Fields to then show the Quantity in words in another field and show in the Delivery Slip Report
    
    
    total_demands = fields.Float(string='Total Quantity', store=True, readonly=True, compute='_amount_all')
    
    amount_demands = fields.Float(string='Demands', store=True, readonly=True, compute='_amount_all', tracking=True)
    
    qty_in_words = fields.Char(string='Quantity In Words', compute='get_qty_in_words')
    
    
    
    @api.depends('move_ids_without_package.product_uom_qty')
    def _amount_all(self):
        for order in self:
            amount_demands = 0.0
            for line in order.move_ids_without_package:
                amount_demands += line.product_uom_qty
                
            order.update({
                'amount_demands': order.amount_demands,
                'total_demands': amount_demands,
            })
            
            
    @api.depends('total_demands')
    def get_qty_in_words(self):
        for move in self:
            if move.total_demands:
                words = 'Only '
                words += num2words(float(move.total_demands), lang='en')
                move.qty_in_words = words
            else:
                move.qty_in_words = ''