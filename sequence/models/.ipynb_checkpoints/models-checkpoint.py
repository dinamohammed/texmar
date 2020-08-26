# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    state = fields.Selection([
        ('note_order','Note Order'),
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default=lambda self: self._compute_state_company())
    
    def _compute_state_company(self):
        state = None
        if self.env.company.parent_id:
            state = 'note_order'
        else:
            state = 'draft'
        return state
    
#     def _prepare_so(self):
#         self.ensure_one()
#         return {'name' : self.client_order_ref,
#                 'partner_id' : self.partner_id.id,
#                 'partner_invoice_id' : self.partner_invoice_id.id,
#                 'customer_order' : self.customer_order,
#                 'partner_shipping_id' : self.partner_shipping_id.id,
#                 'partner_invoice_id' : self.partner_invoice_id.id,
#                 'sale_order_template_id' : self.sale_order_template_id.id,
#                 'validity_date' : self.validity_date,
#                 'date_order' : self.date_order,
#                 'hide_cancel' : self.hide_cancel,
#                 'stop_cancel_at' : self.stop_cancel_at,
#                 'pricelist_id' : self.pricelist_id.id,
#                 'print_image' : self.print_image,
#                 'image_sizes' : self.image_sizes,
#                 'payment_term_id' : self.payment_term_id.id,
#                 'discount_type' : self.discount_type,
#                 'discount_rate' : self.discount_rate,
#                 'note' : self.note,
#                 'amount_untaxed' : self.amount_untaxed,
#                 'amount_discount' : self.amount_discount,
#                 'amount_tax' : self.amount_tax,
#                 'amount_total' : self.amount_total,
#                 'user_id' : self.user_id.id,
#                 'team_id' : self.team_id.id,
#                 'company_id' : self.company_id.id,
#                 'require_signature' : self.require_signature,
#                 'require_payment' : self.require_payment,
#                 'fiscal_position_id' : self.fiscal_position_id.id,
#                 'analytic_account_id' : self.analytic_account_id.id,
#                 'warehouse_id' : self.warehouse_id.id,
#                 'intercom' : self.intercom.id,
#                 'picking_policy' : self.picking_policy,
#                 'commitment_date' : self.commitment_date,
#                 'origin' : self.origin,
#                 'campaign_id' : self.campaign_id.id,
#                 'medium_id' : self.medium_id.id,
#                 'source_id' : self.source_id.id,
#                 'specs_conditions' : self.specs_conditions,
#                 'signed_by' : self.signed_by,
#                 'signed_on' : self.signed_on,
#                 'signature' : self.signature,
#                }
    
    
    @api.model
    def create(self, vals):
        # if company has parent ie its a Branch
        if self.env.company.parent_id:
            if vals.get('name', _('New')) == _('New'):
                   seq_date = None
                   if 'date_order' in vals:
                       seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
                   if 'company_id' in vals:
                       vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                           'note.order', sequence_date=seq_date) or _('New')
                   else:
                       vals['name'] = self.env['ir.sequence'].next_by_code('note.order', sequence_date=seq_date) or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
            if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
                partner = self.env['res.partner'].browse(vals.get('partner_id'))
                addr = partner.address_get(['delivery', 'invoice'])
                vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
                vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
                vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and
                                                       partner.property_product_pricelist.id)
            result = super(SaleOrder, self).create(vals)
            
        else:
            if vals.get('name', _('New')) == _('New'):
                seq_date = None
                if 'date_order' in vals:
                    seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
                if 'company_id' in vals:
                    vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                        'sale.order', sequence_date=seq_date) or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
            if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
                partner = self.env['res.partner'].browse(vals.get('partner_id'))
                addr = partner.address_get(['delivery', 'invoice'])
                vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
                vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
                vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and
                                                       partner.property_product_pricelist.id)
            result = super(SaleOrder, self).create(vals)
                
        
        return result
