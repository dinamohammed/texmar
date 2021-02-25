# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9


class res_company(models.Model):
    _inherit = "res.company"

    account_check_printing_layout = fields.Selection(string="Check Layout", required=True,
        help="Select the format corresponding to the check paper you will be printing your checks on.\n"
             "In order to disable the printing feature, select 'None'.",
        selection=[
            ('disabled', 'None'),
            ('action_print_check_top', 'check on top'),
            ('action_print_check_middle', 'check in middle'),
            ('action_print_check_bottom', 'check on bottom'),
            ('action_print_qnb_check_top', 'QNB check on top')
        ],
        default="action_print_qnb_check_top")
    
    
class account_payment(models.Model):
    _inherit = "account.payment"
    
    check_owner = fields.Char(string= "Check Owner", help="Give this field a value if you dont want to view the partner name"
                              "in check print out.")
    
    due_date_check = fields.Date("Due Date" , default = fields.Datetime.today())

    def do_print_checks(self):
        if self:
            check_layout = self[0].company_id.account_check_printing_layout
            # A config parameter is used to give the ability to use this check format even in other countries than US, as not all the localizations have one
            if check_layout != 'disabled' and (self[0].journal_id.company_id.country_id.code == 'EG' or bool(self.env['ir.config_parameter'].sudo().get_param('account_check_printing_force_us_format'))):
                self.write({'state': 'sent'})
                return self.env.ref('qnb_check_print.%s' % check_layout).report_action(self)
        return super(account_payment, self).do_print_checks()
    
    
    def print_checks(self):
        """ Check that the recordset is valid, set the payments state to sent and call print_checks() """
        # Since this method can be called via a client_action_multi, we need to make sure the received records are what we expect
        self = self.filtered(lambda r: (r.payment_method_id.code == 'check_printing' or r.payment_method_id.code == 'received_third_check' or r.payment_method_id.code == 'delivered_third_check' or r.payment_method_id.code == 'issue_check' ) and r.state != 'reconciled')

        if len(self) == 0:
            raise UserError(_("Payments to print as a checks must have 'Check' selected as payment method and "
                              "not have already been reconciled"))
        if any(payment.journal_id != self[0].journal_id for payment in self):
            raise UserError(_("In order to print multiple checks at once, they must belong to the same bank journal."))

        if not self[0].journal_id.check_manual_sequencing:
            # The wizard asks for the number printed on the first pre-printed check
            # so payments are attributed the number of the check the'll be printed on.
            last_printed_check = self.search([
                ('journal_id', '=', self[0].journal_id.id),
                ('check_number', '!=', "0")], order="check_number desc", limit=1)
#             next_check_number = self.check_id.name
            next_check_number = last_printed_check and int(last_printed_check.check_number) + 1 or 1

            return {
                'name': _('Print Pre-numbered Checks'),
                'type': 'ir.actions.act_window',
                'res_model': 'print.prenumbered.checks',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'payment_ids': self.ids,
                    'default_next_check_number': next_check_number,
                }
            }
        else:
            self.filtered(lambda r: r.state == 'draft').post()
            return self.do_print_checks()
        
        
    def _check_build_page_info(self, i, p):
        multi_stub = self.company_id.account_check_printing_multi_stub
        return {
            'sequence_number': self.check_number if (self.journal_id.check_manual_sequencing and self.check_number != 0) else 
            False,
            'payment_date': format_date(self.env, self.payment_date),
            'due_date_check': format_date(self.env, self.due_date_check),
            'partner_id': self.partner_id,
            'partner_name': self.partner_id.name,
            'check_owner': self.check_owner,
            'currency': self.currency_id,
            'state': self.state,
            'amount': formatLang(self.env, self.amount, currency_obj=self.currency_id) if i == 0 else 'VOID',
            'amount_in_word': self._check_fill_line(self.check_amount_in_words) if i == 0 else 'VOID',
            'memo': self.communication,
            'stub_cropped': not multi_stub and len(self.invoice_ids) > INV_LINES_PER_STUB,
            # If the payment does not reference an invoice, there is no stub line to display
            'stub_lines': p,
        }