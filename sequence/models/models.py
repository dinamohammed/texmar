# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError



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
        if not self.env.user.branch_id or not self.env.user.branch_ids:
            state = 'note_order'
        else:
            state = 'draft'
        return state
    
    def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = self.env.company.quotation_validity_days
            if days > 0:
                return fields.Date.to_string(datetime.now() + timedelta(days))
        return False
    
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'note_order': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    
    validity_date = fields.Date(string='Expiration', readonly=True, copy=False, 
                                states={'draft': [('readonly', False)],'sent':[('readonly',False)],
                                'note_order':[('readonly',False)]},default=lambda self: self._default_validity_date())
    
    
    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'note_order': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 
                'sale': [('readonly', False)], 'note_order': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                'sale': [('readonly', False)], 'note_order': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, 
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                         'note_order': [('readonly', False)]}, copy=False, default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
                         
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
         'note_order': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")
    
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                                           'note_order': [('readonly', False)]}, default='percent')
                         
    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]
                                                       , 'note_order': [('readonly', False)]})
    is_confirmed = fields.Boolean(default=False)
    def _get_default_require_signature(self):
        return self.env.company.portal_confirmation_sign

    
    def _prepare_so(self):
        self.ensure_one()
        sale_order_line = {}
        for record in self:
               sale_order_line = {
#                    'name' : record.name,
                  'state' : 'draft',
                  'partner_id' : record.partner_id.id,
#                 'partner_invoice_id' : self.partner_invoice_id.id,
#                 'customer_order' : self.customer_order,
#                 'partner_shipping_id' : self.partner_shipping_id.id,
#                 'partner_invoice_id' : self.partner_invoice_id.id,
                  'sale_order_template_id' : record.sale_order_template_id.id,
                  'validity_date' : record.validity_date,
                  'date_order' : record.date_order,
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
                'warehouse_id' : self.warehouse_id.id,
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
                'order_line' : [],
               }
#         raise ValidationError(sale_order_line['name'])
        return sale_order_line
    
    
    def action_confirm_note_order(self):
        for record in self :
            new_sale_order = record._prepare_so()

#             new_sale_order['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
            for line in record.order_line:
                if line._prepare_sol():
                    new_sale_order['order_line'].append((0, 0, line._prepare_sol()))
            record.write({'is_confirmed':True})
        
        sale_order_name = self.create(new_sale_order)
        sale_order_name.write({'name': self.env['ir.sequence'].next_by_code('sale.order') or _('New')})
    
    
    @api.model
    def create(self, vals):
        
        if not self.env.user.branch_id or not self.env.user.branch_ids:
            vals['name'] = self.env['ir.sequence'].with_context().next_by_code('request.order')\
            or _('New')
        else:
            vals['name'] = self.env['ir.sequence'].with_context().next_by_code('note.order')\
            or _('New')
        return super(SaleOrder, self).create(vals)

    
    
    
# class SOLineInherit(models.Model):
#     _name = 'so.lines'
    
#     sale_order_line_ids = fields.One2many('sale.order.line', 'custom_model_id', 'Sale Order Line')
    

    
class SOLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    to_sell = fields.Boolean("Sell")
    
    to_request = fields.Boolean("Request")
    
    custom_model_id = fields.Many2one('so.lines', 'Custom Model')
    
    
    def _prepare_sol(self):
        sol ={}
        
        self.ensure_one()
#         for line in self:
        if self.to_sell:
            sol = {
#                'image_small' : self.image_small,
                'product_id' : self.product_id.id,
                'name' : self.name,
                'analytic_tag_ids' : self.analytic_tag_ids,
#                 'route_id' : self.route_id,
                'product_uom_qty' : self.product_uom_qty,
                'product_uom' : self.product_uom.id,
                'customer_lead' : self.customer_lead,
#                 'product_packaging' : self.product_packaging,
                'price_unit' : self.price_unit,
                'tax_id' : self.tax_id,
#                 'discount' : self.discount,
                'price_subtotal' : self.price_subtotal,
                'sample_date' : self.sample_date,
                'line_delivery_date' : self.line_delivery_date,
                'approval_status' : self.approval_status,
                'line_status' : self.line_status}
                    
#         raise ValidationError(sol['name'])
        return sol



# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
    
    
#     @api.model
#     def create(self, vals):
#         if self.env.company.parent_id:
#             if vals.get('name', 'New') == 'New':
#                 seq_date = None
#                 if 'date_order' in vals:
#                     seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
#                 vals['name'] = self.env['ir.sequence'].next_by_code('request.purchase.order', sequence_date=seq_date) or '/'
#             return super(PurchaseOrder, self).create(vals)
#         else:
#             if vals.get('name', 'New') == 'New':
#                 seq_date = None
#                 if 'date_order' in vals:
#                     seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
#                 vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
#             return super(PurchaseOrder, self).create(vals)

    
    