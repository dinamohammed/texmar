from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import itertools
from operator import itemgetter
import operator

# =====================



class ProductPurchaseLine(models.TransientModel):
    _name ='product.purchase.line'
    
    
    product_ids = fields.Many2many('product.product',string='Products')
    
    
    def get_product_ids(self):
        products = self.env['purchase.order.line'].search([('id','in',self.product_ids.ids)])
        return products
    
    def get_purchase_order(self,product_id):
        po_lines = self.env['purchase.order.line'].search([('product_id','=',product_id)])
        return po_lines
    
    
    def print_pdf(self):
        data={}
        data['form'] = self.read()[0]
        return self.env.ref('sales_compare_report.action_report_sales_compare').report_action(self, data=None)
        