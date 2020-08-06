# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NoteOrder(models.Model):
    _name = 'note.order'
    _inherit = 'sale.order'

