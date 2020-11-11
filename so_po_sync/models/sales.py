# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import logging
_logger = logging.getLogger(__name__)


class so_po_sync(models.Model):
    _inherit = 'sale.order'
    
    stock_picking = fields.Many2one('stock.picking','Picking')
    delivery_states = fields.Selection(string='Delivery States',store=True,readonly=True,related='stock_picking.state')
    
    branch_customer_name = fields.Char(string='Branch Customer Name',readonly=True)
    branch_customer_phone = fields.Char(string='Branch Customer phone',readonly=True)
    branch_payment_terms = fields.Char(string='Branch Payment Term',readonly=True)
    
    branch_delivery_states = fields.Selection([('draft', 'Draft'),
                                               ('done', 'Done'),
                                               ('waiting', 'Waiting Another Operation'),
                                               ('cancel', 'Cancel'),
                                               ('confirmed', 'Waiting'),
                                               ('assigned', 'Ready')],
                                              'Branch Delivery States', readonly=True)
    
    def action_confirm(self):
        super(so_po_sync, self).action_confirm()
        # mentors start
        notes = self.note
        # adding customer name and phone and terms to purchase from sales
        purchase_orders = self.sudo().env['purchase.order'].search([('origin','=',self.name)])
        if purchase_orders:
            for purchase_order in purchase_orders:
                purchase_order.customer_name = self.partner_id['name']
                purchase_order.customer_phone = self.partner_id['mobile']
                purchase_order.notes = notes
                # adding customer name and phone and terms to main sales from purchase
                sales = self.sudo().env['sale.order'].search([('name','=',purchase_order.partner_ref)])
                for sale in sales:
                    sale.branch_customer_name = self.partner_id['name']
                    sale.branch_customer_phone = self.partner_id['mobile']
                    sale.note = notes
                    sale.branch_delivery_states = self.delivery_states
                    sale.add_delivery(purchase_order)
                    # adding customer name and phone and terms to main delivery from main sales
                    deliveries = self.sudo().env['stock.picking'].search([('origin', '=', f'{sale.name}/{purchase_order.name}')])
                    for delivery in deliveries:
                        delivery.branch_customer_name = self.partner_id['name']
                        delivery.branch_customer_phone = self.partner_id['mobile']
                    # adding terms to mo
                    mo = self.sudo().env['mrp.production'].search([('origin', '=', f"{sale.name}/{purchase_order.name}")])
                    mo.notes = notes
                self.add_delivery(purchase_order)
        self.batch_state()
        # mentors end
        return True
    
    def batch_state(self):
        for rec in self:
            lines = rec.order_line
            for line in lines:
                batches = line.batch
                for batch in batches:
                    batch.sudo().write({'state':'reserved'})
    
    def add_delivery(self, purchase):
        #  adding delivery to sale
        sale_name = self.name
        deliveries = self.sudo().env['stock.picking'].search([('origin','=',sale_name)]) \
                     or self.sudo().env['stock.picking'].search([('origin','=',f'{purchase.partner_ref}/{purchase.name}')])
        for delivery in deliveries:
            self.stock_picking = delivery
    
    placeholder = fields.Char(compute='o_change',string='placeholde')
    
    @api.depends('delivery_states')
    def o_change(self):
        self.placeholder = self.delivery_states
        #      the function starts here
        sale_name = self.name
        purchase_orders = self.sudo().env['purchase.order'].search([('origin','=',self.name)])
        for purchase_order in purchase_orders:
            if purchase_order:
                sales = self.sudo().env['sale.order'].search([('name','=',purchase_order.partner_ref)])
                for sale in sales:
                    sale.branch_delivery_states = self.delivery_states
