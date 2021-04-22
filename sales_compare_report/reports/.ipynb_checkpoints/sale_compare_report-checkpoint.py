# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import ValidationError, UserError



class AppointmentReport(models.AbstractModel):
    _name = 'report.sales_compare_report.report_sales_compare_document'
    _description = 'Sales Compare Report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['product_ids']:
            products = self.env['product.product'].search([('id','in',data['form']['product_ids'])])
#             purchase_lines = self.env['purchase.order.line'].read_group(
#                 [['product_id','in',data['form']['product_ids']]],[],groupby=['product_id','order_id'],lazy=False)
            purchase_lines = self.env['purchase.order.line'].search(
                [('product_id','in',data['form']['product_ids'])],order='product_id')
            sale_lines = self.env['sale.order.line'].search(
                [('product_id','in',product_id)],order='product_id')
        else:
            purchase_lines = self.env['purchase.order.line'].search([])
#         raise ValidationError('%s'%purchase_lines[0])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
#         raise ValidationError('%s'%products)
        return {
            'doc_model': 'purchase.order.line',
            'purchase_lines': purchase_lines,
            'products': products,
        }