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
        return self.product_ids.ids
    
    def get_purchase_order(self,product_ids):
        pass
        
#         purchase_orders = self.env['purchase_order_line'].groupby()
        