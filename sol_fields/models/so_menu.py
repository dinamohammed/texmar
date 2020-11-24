# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SOLineInherit(models.Model):
    _name = 'so.lines'
    
    sale_order_line_ids = fields.One2many('sale.order.line', 'custom_model_id', 'Sale Order Line')
    

    
