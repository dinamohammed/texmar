# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models, api, fields, _


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    
    @api.model
    def _get_quotation_sequence(self):
        seq_id = self.env['ir.sequence'].search([('code', '=', 'sale.order')], limit=1)
        if seq_id:
            return seq_id.id
        else:
            return False

    sale_number = fields.Many2one('ir.sequence', string='Sequence', required=True,
                                  domain=[('code', 'in', ['sale.order', 'sale.quotation'])],
                                  default=_get_quotation_sequence)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if vals.get('sale_number'):
                obj_seq = self.env['ir.sequence'].browse(vals.get('sale_number'))
                if obj_seq.code == 'sale.order':
                    vals['name'] = self.env['ir.sequence'].next_by_code(
                        'sale.order') or '/'
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code(
                        'sale.quotation') or '/'
        return super(SaleOrderInherit, self).create(vals)

    def _action_confirm(self):
        super(SaleOrderInherit, self)._action_confirm()
        seq_obj = self.env['ir.sequence']
        sale_order_sequence_id = seq_obj.search([('code', '=', 'sale.order')])
        if sale_order_sequence_id:
            for order in self:
                if order.sale_number.id != sale_order_sequence_id.id:
                    order.sale_number = sale_order_sequence_id.id
                    order.name = seq_obj.next_by_code('sale.order')

