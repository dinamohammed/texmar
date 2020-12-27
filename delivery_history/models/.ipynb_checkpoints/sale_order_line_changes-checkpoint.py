# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class SaleOrderLine(models.Model):
    
    _inherit = "sale.order.line"
    
    deliver_date_history_id = fields.One2many('sale.delivery.date.history','sale_order_line_ids')
    
    @api.onchange('line_delivery_date')
    def onchange_delivery_date(self):
        if self.line_delivery_date:
            self.env['sale.delivery.date.history'].create({'sale_order_line_ids': self.ids[0],
                'delivery_date': self.line_delivery_date,
                'editing_date': datetime.date.today(),})
        
    
    def action_view_history_delivery(self):
        action = self.env.ref('delivery_history.action_view_delivered_per_line').read()[0]
        sol_ids = self.mapped('deliver_date_history_id')
#         if len(pickings) > 1:
        action['domain'] = [('id', 'in', sol_ids.ids)]
#         action['context'] = dict(self._context, default_origin=self.name, create=False)
        return action
    

    
class SaleOrder(models.Model):
    
    _inherit = "sale.order"
    
    
    

        
#     def action_view_delivered_per_line(self):
#         pass