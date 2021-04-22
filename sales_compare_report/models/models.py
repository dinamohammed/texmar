# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_reference = fields.Char(related = "product_id.default_code", store = True)
    product_name = fields.Char(related = "product_id.name", store = True)
    product_qty_on_hand = fields.Float(related = "product_id.qty_available", store = True)
    remaining_qty = fields.Char("Remaining Qty", compute = "_return_remaining_qty", store = True)
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
    approve_date = fields.Datetime(related = "order_id.date_approve")
    product_market = fields.Integer("Market")
    product_gallery = fields.Integer("Gallery")
    product_dealer = fields.Integer("Dealer")
    
    @api.depends('product_qty','qty_received')
    def _return_remaining_qty(self):
        for line in self:
            line.remaining_qty = line.product_qty - line.qty_received
    
    @api.depends('product_id')
    def _return_product_color(self):
        for line in self:
            product = line.product_id
            color_attr = self.env.ref('product.product_attribute_2')
            for attribute in product.product_template_attribute_value_ids:
                if attribute.attribute_id == color_attr \
                            and attribute.product_attribute_value_id:
                    line.product_color = attribute.product_attribute_value_id.name.split('-')[1]
                    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
    @api.depends('product_template_attribute_value_ids')
    def _return_product_color(self):
        for line in self:
            color_attr = self.env.ref('product.product_attribute_2')
            for attribute in line.product_template_attribute_value_ids:
                if attribute.attribute_id == color_attr \
                            and attribute.product_attribute_value_id:
                    line.product_color = attribute.product_attribute_value_id.name.split('-')[1]
                                        

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    is_market = fields.Boolean('Market', compute = '_give_values', store = True)
    is_gallery = fields.Boolean('Gallery', compute = '_give_values', store = True)
    is_dealer = fields.Boolean('Dealer', compute = '_give_values', store = True)
    
    @api.depends('branch_id')
    def _give_values(self):
        for order in self:
            if order.branch_id:
                order.is_gallery = True
            else:
                order.is_market = True
    