# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import datetime, timedelta



# class SaleOrderLine(models.Model):
    
#     _inherit = 'sale.order.line'
        
#     less_validate = fields.Boolean('Less Validate' ,compute = '_compute_less_validate' ,readonly = True)
    
#     virtual_available_at_date = fields.Float('Available Qty',compute='_compute_qty_at_date')

    
#     @api.depends('less_validate')
#     def _compute_less_validate(self):
#         for record in self:
#             if record.virtual_available_at_date < record.product_uom_qty :
#                 record.less_validate = True
                
    
#     @api.depends('product_id', 'customer_lead', 'product_uom_qty', 'order_id.commitment_date')
#     def _compute_qty_at_date(self):
#         """ Compute the quantity forecasted of product at delivery date. There are
#         two cases:
#          1. The quotation has a commitment_date, we take it as delivery date
#          2. The quotation hasn't commitment_date, we compute the estimated delivery
#             date based on lead time"""
#         qty_processed_per_product = defaultdict(lambda: 0)
#         grouped_lines = defaultdict(lambda: self.env['sale.order.line'])
#         # We first loop over the SO lines to group them by warehouse and schedule
#         # date in order to batch the read of the quantities computed field.
        
#         warehouse_id_m = self.sudo().env['stock.warehouse'].search([('code','=','123')], limit=1)
#         raise ValidationError(_('Warehouse ' % warehouse_id_m))

#         for line in self:
#             if not line.display_qty_widget:
#                 continue
#             line.warehouse_id = warehouse_id_m
#             if line.order_id.commitment_date:
#                 date = line.order_id.commitment_date
#             else:
#                 confirm_date = line.order_id.date_order if line.order_id.state in ['sale', 'done'] else datetime.now()
#                 date = confirm_date + timedelta(days=line.customer_lead or 0.0)
#             grouped_lines[(line.warehouse_id.id, date)] |= line

#         treated = self.browse()
#         for (warehouse, scheduled_date), lines in grouped_lines.items():
#             #raise ValidationError(_('warehouse' % warehouse))
#             product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, warehouse=warehouse).read([
#                 'qty_available',
#                 'free_qty',
#                 'virtual_available',
#             ])
#             qties_per_product = {
#                 product['id']: (product['qty_available'], product['free_qty'], product['virtual_available'])
#                 for product in product_qties
#             }
#             for line in lines:
#                 line.scheduled_date = scheduled_date
#                 qty_available_today, free_qty_today, virtual_available_at_date = qties_per_product[line.product_id.id]
#                 line.qty_available_today = qty_available_today - qty_processed_per_product[line.product_id.id]
#                 line.free_qty_today = free_qty_today - qty_processed_per_product[line.product_id.id]
#                 line.virtual_available_at_date = virtual_available_at_date - qty_processed_per_product[line.product_id.id]
#                 qty_processed_per_product[line.product_id.id] += line.product_uom_qty
#             treated |= lines
#         remaining = (self - treated)
#         remaining.virtual_available_at_date = False
#         remaining.scheduled_date = False
#         remaining.free_qty_today = False
#         remaining.qty_available_today = False
#         remaining.warehouse_id = False
                


    
    
#     def action_confirm(self):
#         if self._get_forbidden_state_confirm() & set(self.mapped('state')):
#             raise UserError(_(
#                 'It is not allowed to confirm an order in the following states: %s'
#             ) % (', '.join(self._get_forbidden_state_confirm())))

#         for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
#             order.message_subscribe([order.partner_id.id])
#         self.write({
#             'state': 'sale',
#             'date_order': fields.Datetime.now()
#         })
        
#         for line in self.order_line:
#             if line.virtual_available_at_date < line.product_uom_qty:
#                 raise ValidationError(_('Cannot confirm Order Available qty of product: %s is less than Quantity' % line.name))
                
#         self._action_confirm()
#         if self.env.user.has_group('sale.group_auto_done_setting'):
#             self.action_done()
#         return True


