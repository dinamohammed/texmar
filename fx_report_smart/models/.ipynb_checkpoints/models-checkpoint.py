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
    
    
    def _get_report_name(self):
        return _('FX Report')
    
    def get_header(self, options):
        start_date = format_date(self.env, options['date']['date_from'])
        end_date = format_date(self.env, options['date']['date_to'])
        return [
            [
                {'name': ''},
                {'name': _('Caracteristics'), 'colspan': 4},
                {'name': _('Assets'), 'colspan': 4},
                {'name': _('Depreciation'), 'colspan': 4},
                {'name': _('Book Value')},
            ],
            [
                {'name': ''},  # Description
                {'name': _('Acquisition Date'), 'class': 'text-center'},  # Caracteristics
                {'name': _('First Depreciation'), 'class': 'text-center'},
                {'name': _('Method'), 'class': 'text-center'},
                {'name': _('Rate'), 'class': 'number', 'title': _('In percent.<br>For a linear method, the depreciation rate is computed per year.<br>For a degressive method, it is the degressive factor'), 'data-toggle': 'tooltip'},
                {'name': start_date, 'class': 'number'},  # Assets
                {'name': _('+'), 'class': 'number'},
                {'name': _('-'), 'class': 'number'},
                {'name': end_date, 'class': 'number'},
                {'name': start_date, 'class': 'number'},  # Depreciation
                {'name': _('+'), 'class': 'number'},
                {'name': _('-'), 'class': 'number'},
                {'name': end_date, 'class': 'number'},
                {'name': '', 'class': 'number'},  # Gross
            ],
        ]
    
    
    