# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class po_cancel(models.Model):
    _inherit='purchase.order'

    def cancel_po_so(self):
        alll = self.sudo().env['sale.order'].search([('name','=',self.partner_ref)])
        for product in alll:
            product.action_cancel()

    
    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(_("Unable to cancel this purchase order. You must first cancel the related vendor bills."))
        self.cancel_po_so()
        self.write({'state': 'cancel'})



