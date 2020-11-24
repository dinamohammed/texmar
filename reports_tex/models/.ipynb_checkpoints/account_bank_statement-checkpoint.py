# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from num2words import num2words
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    amount_in_words = fields.Char(string="Amount in Words",_compute='_onchange_amount')

    @api.onchange('amount', 'journal_currency_id')
    def _onchange_amount(self):
        for pay in self:
            amount_text = self.currency_id.with_context({'lang': self.env.user.lang}).amount_to_text(
			pay.amount)
            if pay.env.user.lang in ['ar', 'ar_SY', 'ar_001']:
                amount_in_words = "%s %s" % (amount_text, "فقط")
                amount_in_words = str(amount_in_words).replace('Euros', 'يورو')
                amount_in_words = str(amount_in_words).replace('Dollars', 'دولارات')
                amount_in_words = str(amount_in_words).replace('Dollar', 'دولار')
                amount_in_words = str(amount_in_words).replace('Cents', 'سنتاً')
                amount_in_words = str(amount_in_words).replace('Cent', 'سنت')
                amount_in_words = str(amount_in_words).replace('Pound', 'جنيهاً')
                amount_in_words = str(amount_in_words).replace('Pounds', 'جنيهات')
                amount_in_words = str(amount_in_words).replace('Piastres', 'قرشاً')
            else:
                amount_in_words = amount_text + ' only'

            pay.amount_in_words = amount_in_words
        return res
