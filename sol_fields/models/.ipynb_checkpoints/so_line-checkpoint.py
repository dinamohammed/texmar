# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SOLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    to_sell = fields.Boolean("Sell")
    
    to_request = fields.Boolean("Request")
