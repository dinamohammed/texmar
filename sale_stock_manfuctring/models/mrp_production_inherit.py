# -*- coding: utf-8 -*-
from odoo import models, fields, api
from itertools import groupby


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    size_of_pieces = fields.Float(string='Size of Pieces', readonly=1)
    qty_producing = fields.Float(string='Currently Produced Quantity', digits='Product Unit of Measure')
    quantity_difference = fields.Float("Quantity Difference", readonly=1)
    piece1 = fields.Integer(readonly=1)
    piece2 = fields.Integer(readonly=1)
    piece3 = fields.Integer(readonly=1)
    piece4 = fields.Integer(readonly=1)
    piece5 = fields.Integer(readonly=1)
    piece6 = fields.Integer(readonly=1)
    piece7 = fields.Integer(readonly=1)
    piece8 = fields.Integer(readonly=1)
    piece9 = fields.Integer(readonly=1)
    piece10 = fields.Integer(readonly=1)
    piece11 = fields.Integer(readonly=1)
    piece12 = fields.Integer(readonly=1)
    piece13 = fields.Integer(readonly=1)
