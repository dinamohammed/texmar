# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_reference = fields.Char(related = "product_id.default_code", store = True)
    product_name = fields.Char(related = "product_id.name", store = True)
    product_qty_on_hand = fields.Float(related = "product_id.qty_available", store = True)
    remaining_qty = fields.Char("Remaining Qty", compute = "_return_remaining_qty", store = True)
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
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
                                        
                    