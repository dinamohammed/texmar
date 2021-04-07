# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_reference = fields.Char(related = "product_id.default_code", store = True)
    product_name = fields.Char(related = "product_id.name", store = True)
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
    @api.depends('product_id')
    def _return_product_color(self):
        for line in self:
            product = line.product_id
            
            for attribute in product.product_template_attribute_value_ids:
                color = attribute.product_attribute_value_id.name
                line.product_color = color
                    