# -*- coding: utf-8 -*-

from odoo import models, fields, api

class so_po_sync(models.Model):
    _inherit = 'purchase.order'

    customer_name = fields.Char(string='Customer Name',readonly=True)
    customer_phone = fields.Char(string='Customer phone',readonly=True)
