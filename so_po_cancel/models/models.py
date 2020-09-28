# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class so_cancel(models.Model):
    _inherit='sale.order'
    # mentors
    def cancel_po_so(self):
        alll = self.sudo().env['purchase.order'].search([('origin','=',self.name)])
        for purchase in alll:
            purchase.button_cancel()


    def action_cancel(self):
        documents = None
        for sale_order in self:
            if sale_order.state == 'sale' and sale_order.order_line:
                sale_order_lines_quantities = {order_line: (order_line.product_uom_qty, 0) for order_line in sale_order.order_line}
                documents = self.env['stock.picking']._log_activity_get_documents(sale_order_lines_quantities, 'move_ids', 'UP')
        self.mapped('picking_ids').action_cancel()
        if documents:
            filtered_documents = {}
            for (parent, responsible), rendering_context in documents.items():
                if parent._name == 'stock.picking':
                    if parent.state == 'cancel':
                        continue
                filtered_documents[(parent, responsible)] = rendering_context
            self._log_decrease_ordered_quantity(filtered_documents, cancel=True)
#           mentors start
            self.cancel_po_so()
#           mentors end
        return super(so_cancel, self).action_cancel()  

class po_cancel(models.Model):
    _inherit='purchase.order'

    #mentors
    def cancel_po_so(self):
        alll = self.sudo().env['sale.order'].search([('name','=',self.partner_ref)])
        recipts = self.sudo().env['stock.picking'].search([('origin','=',self.name)])

        for recipt in recipts:
            recipt.action_cancel()

        for sale in alll:
            mo = self.sudo().env['mrp.production'].search([('origin','=',f"{sale.name}/{self.name}")])
            if mo:
                mo.action_cancel()
            sale.action_cancel()
  
    def button_cancel(self):
        for order in self:
            order.write({'state':'cancel'})
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(_("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

#       mentors start 
        self.cancel_po_so()
#       mentors end       



