# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    so_po_ref = fields.Char(related = 'picking_id.origin',store=True)
