# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


# Start Cancel operation
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    line_status = fields.Selection([('open', 'Open'),
                                    ('closed', 'Closed'),
                                    ('cancel', 'Cancel')], "Status", default='open')

    @api.onchange('line_status')
    def o_change(self):
        order_name = self.order_id.name
        client_ref = self.order_id.client_order_ref
        deliveries = self.sudo().env['stock.picking'].search([('origin', '=', order_name)]) \
                     or self.sudo().env['stock.picking'].search([('origin', '=', f'{order_name}/{client_ref}')])
        for delivery in deliveries:
            products = delivery.move_ids_without_package
            for product in products:
                if product.name == self.name and self.line_status == 'cancel':
                    product.product_uom_qty = 0


# End Cancel operation


# # Start cloths parameter
# class Product(models.Model):
#     _inherit = 'product.template'

#     texmar_weight = fields.Many2one('texmar.weight', string='Discontin')
#     manufacture_type_id = fields.Many2one('product.manufacture.type', "Sample Box")


# class TexmarWeight(models.Model):
#     _name = 'texmar.weight'

#     name = fields.Char('Name')
