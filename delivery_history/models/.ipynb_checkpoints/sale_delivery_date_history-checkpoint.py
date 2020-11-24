# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class SaleDeliveryDateHistory(models.Model):
    
    _name = "sale.delivery.date.history"
    
    
    sale_order_line_ids = fields.Many2one('sale.order.line', string='Sale Order Lines')
    delivery_date = fields.Date('Delivery Date', store = True)
    editing_date = fields.Date('Editing Date', default = datetime.date.today(), required = True)
    
    