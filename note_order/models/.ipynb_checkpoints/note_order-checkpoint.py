# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NoteOrder(models.Model):
    _name = 'note.order'
    _inherit = 'sale.order'
    
    
    transaction_ids = fields.Many2many('payment.transaction', 'note_order_transaction_rel', 'note_order_id', 'transaction_id',
                                       string='Transactions', copy=False, readonly=True)
    
