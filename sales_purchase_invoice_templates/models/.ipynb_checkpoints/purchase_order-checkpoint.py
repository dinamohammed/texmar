# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    custom_template_id = fields.Many2one('custom.template',string = "Template")
    
