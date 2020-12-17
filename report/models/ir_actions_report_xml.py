# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    paperformat_id = fields.Many2one('report.paperformat', 'Paper format')
    print_report_name = fields.Char('Printed Report Name',
        help="This is the filename of the report going to download. Keep empty to not change the report filename. You can use a python expression with the object and time variables.")

