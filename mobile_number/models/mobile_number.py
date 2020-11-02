# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import ValidationError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    # When the Country is Egypt
    @api.constrains('mobile')
    def _onchange_mobile(self):
        for partner in self:
            if partner.country_id.name == 'Egypt':
                partner.onchange_mobile()
            
    # Only numbers and 11 (16 including spaces) digits only
    def onchange_mobile(self):
        raise ValidationError(_("WARNING: Please Enter a Valid 11 Digit Mobile Naaasusumberr"))
        if self.mobile:
            mobile_trimed_space = self.mobile.replace(" ", "")
            print("Number withou space: ", mobile_trimed_space, len(mobile_trimed_space))
            if len(mobile_trimed_space) != 11:
                raise ValidationError(_("WARNING: Please Enter a Valid 11 Digit Mobile Number"))
            digits = [' ', '+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for i in list(self.mobile):
                if i not in digits:
                    raise ValidationError("WARNING: Mobile Numbers %s , Should only contain Numbers"
                                          % self.mobile)
                
    @api.constrains('mobile')
    def mobile_unique_constrain(self):
        for partner in self:
            if partner.ref and self.env['res.partner'].search_count([('mobile', '=', partner.mobile)]) > 1:
                raise Warning(_("WARNING: Another Contact with this Mobile Number Already Exists"))
