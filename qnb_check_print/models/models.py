# -*- coding: utf-8 -*-

from odoo import models, api, fields

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

    def do_print_checks(self):
        if self:
            check_layout = self[0].company_id.account_check_printing_layout
            # A config parameter is used to give the ability to use this check format even in other countries than US, as not all the localizations have one
            if check_layout != 'disabled' and (self[0].journal_id.company_id.country_id.code == 'US' or bool(self.env['ir.config_parameter'].sudo().get_param('account_check_printing_force_us_format'))):
                self.write({'state': 'sent'})
                return self.env.ref('qnb_check_print.%s' % check_layout).report_action(self)
        return super(account_payment, self).do_print_checks()