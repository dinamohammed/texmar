# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
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
