# -*- coding: utf-8 -*-

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move"
    
    @api.depends('line_ids.discount')
    def _get_discount_amount_lines(self):
        for move in self:
            amount_discount_line = 0
            for line in move.line_ids:
                if line.discount:
                    amount = (line.quantity*line.price_unit)*(line.discount/100.0)
                    amount_discount_line = amount_discount_line + amount
            move.update({
                'amount_discount_line': amount_discount_line,
            })
    
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)]}, default='percent')
    discount_rate = fields.Float('Discount Amount', digits=(16, 2), readonly=True,
                                 states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',
                                      track_visibility='always')
    
    amount_discount_line = fields.Monetary(string='Discount Lines', store=True, readonly=True,
                                           compute='_get_discount_amount_lines',
                                      digits=dp.get_precision('Account'), track_visibility='always')
    
    
    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state')
    def _compute_amount(self):

        invoice_ids = [move.id for move in self if move.id and move.is_invoice(include_receipts=True)]
        self.env['account.payment'].flush(['state'])
        if invoice_ids:
            self._cr.execute(
                '''
                    SELECT move.id
                    FROM account_move move
                    JOIN account_move_line line ON line.move_id = move.id
                    JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
                    JOIN account_move_line rec_line ON
                        (rec_line.id = part.credit_move_id AND line.id = part.debit_move_id)
                        OR
                        (rec_line.id = part.debit_move_id AND line.id = part.credit_move_id)
                    JOIN account_payment payment ON payment.id = rec_line.payment_id
                    JOIN account_journal journal ON journal.id = rec_line.journal_id
                    WHERE payment.state IN ('posted', 'sent')
                    AND journal.post_at = 'bank_rec'
                    AND move.id IN %s
                ''', [tuple(invoice_ids)]
            )
            in_payment_set = set(res[0] for res in self._cr.fetchall())
        else:
            in_payment_set = {}

        for move in self:
            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id:
                    currencies.add(line.currency_id)

                # Untaxed amount.
                if (move.is_invoice(include_receipts=True) and not line.exclude_from_invoice_tab) \
                        or (move.type == 'entry' and line.debit and not line.tax_line_id):
                    total_untaxed += line.balance
                    total_untaxed_currency += line.amount_currency

                # Tax amount.
                if line.tax_line_id:
                    total_tax += line.balance
                    total_tax_currency += line.amount_currency

                # Residual amount.
                if move.type == 'entry' or line.account_id.user_type_id.type in ('receivable', 'payable'):
                    total_residual += line.amount_residual
                    total_residual_currency += line.amount_residual_currency

            total = total_untaxed + total_tax
            total_currency = total_untaxed_currency + total_tax_currency

            if move.type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
                ###### Add discount ####
            amount_discount = 0.0
            if move.discount_type :
                if move.discount_type == 'amount':
                    total_untaxed = total_untaxed - move.discount_rate
                    amount_discount = move.discount_rate
                elif move.discount_type == 'percent':
                    amount_discount = total_untaxed*(move.discount_rate/100)
                    total_untaxed = total_untaxed*((100-move.discount_rate)/100)
            self._get_discount_amount_lines()
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = -total
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id
            is_paid = currency and currency.is_zero(move.amount_residual) or not move.amount_residual

            # Compute 'invoice_payment_state'.
            if move.state == 'posted' and is_paid:
                if move.id in in_payment_set:
                    move.invoice_payment_state = 'in_payment'
                else:
                    move.invoice_payment_state = 'paid'
            else:
                move.invoice_payment_state = 'not_paid'