# -*- coding: utf-8 -*-

from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from odoo.exceptions import ValidationError
from datetime import timedelta

class ReportPartnerLedger(models.Model):
    _inherit = 'account.partner.ledger'
    _name = 'account.partner.ledger.edited'

    def _get_columns_name(self, options):
        columns = [
            {},
            {},
            {},
            {'name': _('Ref')},
            {},
            {},
            {'name': _('Initial Balance'), 'class': 'number'},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'}]

        if self.user_has_groups('base.group_multi_currency'):
            columns.append({})

        columns.append({'name': _('Balance'), 'class': 'number'})

        return columns

    @api.model
    def _get_lines(self, options, line_id=None):
        offset = int(options.get('lines_offset', 0))
        remaining = int(options.get('lines_remaining', 0))
        balance_progress = float(options.get('lines_progress', 0))
        def mod_lines(arr):
                for line in arr:
                #checking if this line carries values
                  if 'caret_options' in line:
                #getting the sql id of the payment
                    identity = line['payment'] or line['account']
                #selecting the payment depending on the sql id
                    payment = self.sudo().env['account.payment'].search([('id','=',identity)])
                    # checking if this is issue check method
                    if payment['payment_method_id'].name == 'Issue Check':
                        #getting the check no
                        check_no = payment['check_id'].name
                        payment_method = payment['payment_method_id'].name
                        payment_sequance = payment.name
                        #overriding ref string
                        line['columns'][2]['name'] = f'{payment_method}/{check_no}/{payment_sequance}'
                     
                    elif payment['payment_method_id'].name == 'Bank':
                        payment_method = payment['payment_method_id'].name
                        payment_sequance = payment.name
                        trans_no = payment['bank_account_number']
                        #overriding ref string
                        line['columns'][2]['name'] = f'{payment_method}/{trans_no}/{payment_sequance}'

                    elif payment['payment_method_id'].name == 'Visa':
                        payment_method = payment['payment_method_id'].name
                        payment_sequance = payment.name
                        visa_no = payment['visa_account_number']
                        #overriding ref string
                        line['columns'][2]['name'] = f'{payment_method}/{visa_no}/{payment_sequance}'

                    else:
                        payment_method = payment['payment_method_id'].name
                        payment_sequance = payment.name
                        #overriding ref string
                        line['columns'][2]['name'] = f'{payment_method}/{payment_sequance}'

                #making this values empty 
                    line['columns'][0]['name'] = ''
                    line['columns'][1]['name'] = ''
                    line['columns'][3]['name'] = ''
                    line['columns'][4]['name'] = ''
                return arr
        if offset > 0:
            lines = self._load_more_lines(options, line_id, offset, remaining, balance_progress)
                
            return mod_lines(lines)
        else:
            # Case the whole report is loaded or a line is expanded for the first time.
            lines = self._get_partner_ledger_lines(options, line_id=line_id)
                
            return mod_lines(lines)


    @api.model
    def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):
        if aml['payment_id']:
            caret_type = 'account.payment'
        elif aml['move_type'] in ('in_refund', 'in_invoice', 'in_receipt'):
            caret_type = 'account.invoice.in'
        elif aml['move_type'] in ('out_refund', 'out_invoice', 'out_receipt'):
            caret_type = 'account.invoice.out'
        else:
            caret_type = 'account.move'

        date_maturity = aml['date_maturity'] and format_date(self.env, fields.Date.from_string(aml['date_maturity']))
        columns = [
            {'name': aml['journal_code']},
            {'name': aml['account_code']},
            {'name': self._format_aml_name(aml['name'], aml['ref'], aml['move_name'])},
            {'name': date_maturity or '', 'class': 'date'},
            {'name': aml['full_rec_name'] or ''},
            {'name': self.format_value(cumulated_init_balance), 'class': 'number'},
            {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            if aml['currency_id']:
                currency = self.env['res.currency'].browse(aml['currency_id'])
                formatted_amount = self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True)
                columns.append({'name': formatted_amount, 'class': 'number'})
            else:
                columns.append({'name': ''})
        columns.append({'name': self.format_value(cumulated_balance), 'class': 'number'})
        return {
            'id': aml['id'],
            'parent_id': 'partner_%s' % partner.id,
            'name': format_date(self.env, aml['date']),
            'class': 'date',
            'columns': columns,
            'caret_options': caret_type,
            'level': 4,
            # making this function return the sql id
            'payment':aml['payment_id'],
            #providing an error 
            'account':aml['account_id']
        }