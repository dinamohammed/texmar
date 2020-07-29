# -*- coding: utf-8 -*-

from odoo import models, fields, api


class payment_method(models.Model):
    _inherit = 'account.payment'
    
    #Incoming Payment: Bank Account Number
    bank_account_number = fields.Char(string='Transfer Number', readonly=False)
    #Incoming Payment: Visa Number
    visa_account_number = fields.Char(string='Visa Number', readonly=False)

    
 

