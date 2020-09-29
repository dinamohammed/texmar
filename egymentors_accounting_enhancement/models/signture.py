from odoo import models, api, fields


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    name_sig = fields.Boolean('Name Signture',default=True)
    id_sig = fields.Boolean('ID Signture',default=True)
    signture_sig = fields.Boolean('Signture',default=True)
    accounting_sig = fields.Boolean('Accounting Signture',default=True)
    ledger_sig = fields.Boolean('Genral Ledger Signture',default=True)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'
    
    total_with_tax = fields.Float(compute='_calc_total_tax', store=True)
    
    @api.depends('tax_ids', 'price_subtotal')
    def _calc_total_tax(self):
        for line in self:
            line_sum = 0
            for tax in line.tax_ids:
                line_sum += tax.amount
            if line_sum == 0:
                line.total_with_tax = 0
            else:
                line.total_with_tax = (line_sum/100)*line.price_subtotal + line.price_subtotal
