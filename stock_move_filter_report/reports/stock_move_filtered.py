# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class StockMoveDelivery(models.TransientModel):
    _name = 'stock.move.filter'

    product_id = fields.Many2one('product.product', "Filter Product", required=True,
                                 help=_("Filter moves with filtered product"))

    def action_filter(self):
        move_ids = self.env['stock.move'].search([('product_id', '=', self.product_id.id)])
        action = self.env.ref('stock_move_filter_report.act_product_stock_move_mentors').read()[0]
        action['domain'] = [('id', 'in', move_ids.mapped('id'))]
        print("action['domain']: ", action['domain'])
        return action