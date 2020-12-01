# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')
    amount_discount_line = fields.Monetary(string='Discount Lines', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')
    
#     amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
#                                    track_visibility='always')
    
    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
#     amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
#                                      track_visibility='always')
#     amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
#                                  track_visibility='always')
#     amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
#                                    track_visibility='always')
    
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='percent')
    
    ###### Here we create only Gobal Discount ##########
    
    @api.onchange('discount_type','discount_rate',)
    def _amount_all(self):
        if self.discount_type :
            if self.discount_type == 'amount':
                self.amount_untaxed -= self.discount_rate
                self.amount_discount = self.discount_rate
            elif self.discount_type == 'percent':
                self.amount_discount = self.amount_untaxed*(self.discount_rate/100)
                self.amount_untaxed = self.amount_untaxed*((100-self.discount_rate)/100)
        
        for line in self:
            if line.discount:
                amount = (line.product_uom_qty*line.price_unit)*(line.discount/100)
                self.amount_discount_line += amount