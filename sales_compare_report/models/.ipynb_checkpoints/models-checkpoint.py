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
                    
                    
                    
    ############# Function called in preparation report ############
    
    def get_lines(self):
#         product_ids = self.get_product_ids()
#         result = []
#         if product_ids:
#             in_lines = self.in_lines(product_ids)
#             out_lines = self.out_lines(product_ids)
#             lst = in_lines + out_lines
#             new_lst = sorted(lst, key=itemgetter('product'))
#             groups = itertools.groupby(new_lst, key=operator.itemgetter('product'))
#             result = [{'product': k, 'values': [x for x in v]} for k, v in groups]
#             for res in result:
#                 print 
#                 l_data = res.get('values')
#                 new_lst = sorted(l_data, key=itemgetter('date'))
#                 print ("")
#                 res['values'] = new_lst

        return result
                                        
                    