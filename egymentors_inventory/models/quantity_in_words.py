# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class QuantityInWords(models.Model):
    _inherit = 'stock.move'
    
    quantity_in_words = 