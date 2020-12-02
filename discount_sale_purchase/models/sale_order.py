# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
        ###### Here we create only Gobal Discount ##########
    
#     @api.onchange('discount_type','discount_rate','order_line')
#     def discount_amount(self):
#         self._amount_all()
#         amount_untaxed = 0
#         amount_discount = 0
#         for order in self:
#             amount_untaxed = order.amount_untaxed
#             if order.discount_type :
#                 if order.discount_type == 'amount':
#                     amount_untaxed = amount_untaxed - order.discount_rate
#                     amount_discount = order.discount_rate
#                 elif order.discount_type == 'percent':
#                     amount_discount = amount_untaxed*(order.discount_rate/100)
#                     amount_untaxed = amount_untaxed*((100-order.discount_rate)/100)
#                 order.update({
#                     'amount_untaxed': amount_untaxed,
#                     'amount_discount': amount_discount,
#                     'amount_total': amount_untaxed + order.amount_tax,
#                 })            
                    
        ###### Here we create only Total Lines of Discount ##########
   #@api.onchange('order_line.discount','order_line.price_subtotal'     
    @api.onchange('order_line')
    def _get_discount_lines(self):
        for order in self:
            amount_discount_line = 0
            for line in order.order_line:
                if line.discount:
                    amount = (line.product_uom_qty*line.price_unit)*(line.discount/100.0)
                    amount_discount_line = amount_discount_line + amount
            order.update({
                'amount_discount_line': amount_discount_line,
            })
    
    
    amount_discount_line = fields.Monetary(string='Discount Lines', store=True, readonly=True,
                                           compute='_get_discount_lines',
                                      digits=dp.get_precision('Account'), track_visibility='always')

    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
    
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='percent')
    
############################# ADD Amounts already available in sales module ######################
    @api.onchange('discount_type','discount_rate','order_line')
    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            self._get_discount_lines()
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            if order.discount_type :
                if order.discount_type == 'amount':
                    amount_untaxed = amount_untaxed - order.discount_rate
                    amount_discount = order.discount_rate
                elif order.discount_type == 'percent':
                    amount_discount = amount_untaxed*(order.discount_rate/100)
                    amount_untaxed = amount_untaxed*((100-order.discount_rate)/100)
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_discount': amount_discount,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

            
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')
    
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')
    
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return invoice_vals

