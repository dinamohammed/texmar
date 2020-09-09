# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from num2words import num2words


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_qty_in_words = fields.Char(string='Quantity In Words', compute='get_product_qty_in_words')

    @api.depends('product_uom', 'product_uom_qty')
    def get_product_qty_in_words(self):
        for move in self:
            if move.product_uom_qty and move.product_uom:
                words = 'Only '
                words += num2words(float(move.product_uom_qty), lang='en')
                words += ' ' + str(move.product_uom.name)
                move.product_qty_in_words = words
            else:
                move.product_qty_in_words = ''
