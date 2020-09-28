# -*- coding: utf-8 -*-
from odoo import models, fields, api
from itertools import groupby


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    mo_id = fields.Many2one('mrp.production',string='MO')

    size_of_pieces = fields.Float(string='Size of Pieces', readonly=1, related='mo_id.size_of_pieces')
    
    def button_validate(self):
        #Super to avoid Overriding
        result = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.sale_id.auto_purchase_order_id and picking.sale_id.auto_generated:
                intercompany_uid = picking.company_id.intercompany_user_id and picking.company_id.intercompany_user_id.id or False

                sale_order_object = self.env['sale.order'].sudo().search(
                    [('name', '=', picking.sale_id.with_user(intercompany_uid).auto_purchase_order_id.origin)])
                
                purchase_order_pickings = self.sudo().search(
                    [('purchase_id', '=', picking.sale_id.with_user(intercompany_uid).auto_purchase_order_id.id)])
                
                sale_order_pickings = self.sudo().search(
                    [('sale_id', '=', sale_order_object.id)])
                
                for move in picking.move_ids_without_package:
                    # Write in purchase order picking in branch company
                    for purchase_picking in purchase_order_pickings:
                        for purchase_move in purchase_picking.move_ids_without_package:
                            if purchase_move.product_id == move.product_id:
                                purchase_move.sudo().write({'size_of_pieces': move.size_of_pieces})
                                break
                                
                    # Write in sale order picking in branch company
                    for sale_picking in sale_order_pickings:
                        for sale_move in sale_order_pickings.move_ids_without_package:
                            if sale_move.product_id == move.product_id:
                                sale_move.sudo().write({'size_of_pieces': move.size_of_pieces})
                                break

        return result    
     

class StockMove(models.Model):
    _inherit = 'stock.move'

    size_of_pieces = fields.Char(string='Size of Pieces', readonly=0)
