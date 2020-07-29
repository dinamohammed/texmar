# -*- coding: utf-8 -*-
from odoo import models, fields, api
from itertools import groupby


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    size_of_pieces = fields.Char(string='Size of Pieces', )

    def button_mark_done(self):
        self.ensure_one()
        res = super(MrpProduction, self).button_mark_done()
        sale_order_object = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
        if sale_order_object:
            for picking_object in sale_order_object.picking_ids:
                picking_object.write({'size_of_pieces': self.size_of_pieces})
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    size_of_pieces = fields.Char(string='Size of Pieces', store=True)
