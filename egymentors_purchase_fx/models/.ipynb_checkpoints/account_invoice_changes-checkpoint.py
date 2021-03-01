# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
# Ahmed Salama Code Start ---->


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.move'
    
    fx_num_id = fields.Many2one(related='invoice_line_ids.fx_num_id',store=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        moves = super(AccountInvoiceInherit, self).create(vals_list)
        for move in moves:
            for line in move.line_ids:
                if line.purchase_line_id:
                    line['fx_num_id'] = line.purchase_line_id.fx_num_id.id
        return moves

    def action_print(self):
        return self.env.ref('account.account_invoices').report_action(self)

    def action_print_without_payment(self):
        return self.env.ref('account.account_invoices_without_payment').report_action(self)

# Ahmed Salama Code End.
class AccountInvoiceLineInherit(models.Model):
    _inherit = 'account.move.line'
    
    fx_num_id = fields.Many2one('fx.number','FX No.', store = True)

#     def _add_fx_number(self):
#         for line in self:
# #             line['fx_num_id'] = line.purchase_line_id.fx_num_id.id
#             line.order_id.write({'fx_num_id': line.purchase_line_id.fx_num_id.id})