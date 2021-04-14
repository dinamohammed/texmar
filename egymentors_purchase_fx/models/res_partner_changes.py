# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
# Ahmed Salama Code Start ---->


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    sequence_id = fields.Many2one('ir.sequence', "Po Sequence")
#     ##################### To be Added in next phase #########################
#     ref = fields.Char('Reference',required=True, index=True, copy=False, default='New', store = True)
    
#     @api.model
#     def create(self, vals):
#         """
#         Add new option to get sequence automatic of ref number
#         :param vals:
#         :return:
#         """
#         if vals.get('ref', 'New') == 'New':
# #             raise ValidationError('%s'%self.env['ir.sequence'].next_by_code('contact.ref'))
#             vals['ref'] = self.env['ir.sequence'].sudo().next_by_code('contact.ref.seq') or '/'
#         result = super(ResPartnerInherit, self).create(vals)

#         return result
    
    @api.constrains('ref')
    def ref_unique_constrain(self):
        for partner in self:
            if partner.ref and self.env['res.partner'].search_count([('ref', '=', partner.ref)]) > 1:
                raise Warning(_("Partner Ref violating unique constrain!!!"))

# Ahmed Salama Code End.

