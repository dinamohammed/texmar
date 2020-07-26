# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError ,ValidationError

from odoo.tools import float_compare


class MrpProductProduceInherit(models.TransientModel):
    _inherit = 'mrp.product.produce'

    quantity_difference = fields.Float("Quantity Difference", compute='get_quantity_difference_value', readonly=1)
    size_of_pieces = fields.Float("Size of Pieces", compute='get_quantity_difference_value', readonly=1, store=True)
    piece1 = fields.Integer()
    piece2 = fields.Integer()
    piece3 = fields.Integer()
    piece4 = fields.Integer()
    piece5 = fields.Integer()
    piece6 = fields.Integer()
    piece7 = fields.Integer()
    piece8 = fields.Integer()
    piece9 = fields.Integer()
    piece10 = fields.Integer()
    piece11 = fields.Integer()
    piece12 = fields.Integer()
    piece13 = fields.Integer()

    def do_produce(self):
        self.ensure_one()
        mrp_production = self.production_id
#         mrp_production = self.env['mrp.production'].browse(self.env.context.get('active_ids'))
        mrp_production.write({
            'piece1': self.piece1,
            'piece2': self.piece2,
            'piece3': self.piece3,
            'piece4': self.piece4,
            'piece5': self.piece5,
            'piece6': self.piece6,
            'piece7': self.piece7,
            'piece8': self.piece8,
            'piece9': self.piece9,
            'piece10': self.piece10,
            'piece11': self.piece11,
            'piece12': self.piece12,
            'piece13': self.piece13,
            'size_of_pieces': self.size_of_pieces,
            'qty_producing': self.qty_producing,
            'quantity_difference': self.quantity_difference, })
            
        returned_origin = mrp_production.origin
        if returned_origin:
            
            origin_array = returned_origin.split('/')
            sales_origin = origin_array[0]
             
            
            sale_order_object = self.sudo().env['sale.order'].search([('name', '=', 
                                                                       sales_origin)], limit=1)
            if sale_order_object:
                for picking_object in sale_order_object.picking_ids:
                    for move in picking_object.move_ids_without_package:
                        if move.product_id.id == mrp_production.product_id.id:
                            move.write({
                                'size_of_pieces': "%s %s %s %s %s %s %s %s %s %s %s %s %s" % (
                                    self.piece1, self.piece2, self.piece3, self.piece4, self.piece5, self.piece6, self.piece7,
                                    self.piece8, self.piece9, self.piece10, self.piece11, self.piece12, self.piece13)
                            })
            purchase_origin = sale_order_object.client_order_ref          
            purchase_order_object = self.sudo().env['purchase.order'].search([('name', '=', purchase_origin)], limit=1)
         #   raise ValidationError(f'origin = {purchase_origin}')
    
            if purchase_order_object:
                for picking_object in purchase_order_object.picking_ids:
                    for move in picking_object.move_ids_without_package:
                        if move.product_id.id == mrp_production.product_id.id:
                            move.write({
                                'size_of_pieces': "%s %s %s %s %s %s %s %s %s %s %s %s %s" % (
                                    self.piece1, self.piece2, self.piece3, self.piece4, self.piece5, self.piece6, self.piece7,
                                    self.piece8, self.piece9, self.piece10, self.piece11, self.piece12, self.piece13)
                            })
            
                            
            initial_sale_origin = purchase_order_object.origin
            initial_sale_order_object = self.sudo().env['sale.order'].search([('name', '=', initial_sale_origin)], limit=1)
    
            if initial_sale_order_object:
                for picking_object in initial_sale_order_object.picking_ids:
                    for move in picking_object.move_ids_without_package:
                        if move.product_id.id == mrp_production.product_id.id:
                            move.write({
                                'size_of_pieces': "%s %s %s %s %s %s %s %s %s %s %s %s %s" % (
                                    self.piece1, self.piece2, self.piece3, self.piece4, self.piece5, self.piece6, self.piece7,
                                    self.piece8, self.piece9, self.piece10, self.piece11, self.piece12, self.piece13)
                            })
    
        return super(MrpProductProduceInherit, self).do_produce()

    @api.depends('piece1', 'piece2', 'piece3', 'piece4', 'piece5', 'piece6', 'piece7', 'piece8', 'piece9',
                 'piece10',
                 'piece11', 'piece12', 'piece13', 'qty_producing')
    @api.onchange('piece1', 'piece2', 'piece3', 'piece4', 'piece5', 'piece6', 'piece7', 'piece8', 'piece9',
                  'piece10',
                  'piece11', 'piece12', 'piece13', 'qty_producing')
    def get_quantity_difference_value(self):
        for wizard in self:
            wizard.size_of_pieces = (
                    wizard.piece1 + wizard.piece2 + wizard.piece3 + wizard.piece4 + wizard.piece5 +
                    wizard.piece6 + wizard.piece7 + wizard.piece8 + wizard.piece9 + wizard.piece10 +
                    wizard.piece11 + wizard.piece12 + wizard.piece13)
            
            wizard.quantity_difference = (
                                                 wizard.piece1 + wizard.piece2 + wizard.piece3 + wizard.piece4 + wizard.piece5 +
                                                 wizard.piece6 + wizard.piece7 + wizard.piece8 + wizard.piece9 + wizard.piece10 +
                                                 wizard.piece11 + wizard.piece12 + wizard.piece13) - wizard.qty_producing
