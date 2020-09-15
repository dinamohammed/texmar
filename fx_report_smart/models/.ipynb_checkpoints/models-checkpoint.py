# -*- coding: utf-8 -*-

from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta


class FxReport(models.AbstractModel):
    _name = 'fx.report.smart'
    _inherit = 'account.report'
    _description = 'Fx Report'
    
    filter_date = {'mode': 'range', 'filter': 'this_year'}
    filter_all_entries = False
    filter_unfold_all = False
    filter_account_type = [
        {'id': 'receivable', 'name': _lt('Receivable'), 'selected': False},
        {'id': 'payable', 'name': _lt('Payable'), 'selected': False},
    ]
    filter_unreconciled = False
    filter_partner = True
    
    
    
    @api.model
    def _get_templates(self):
        templates = super(FxReport, self)._get_templates()
        templates['line_template'] = 'account_reports.line_template_partner_ledger_report'
        return templates
    
    
    