# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import ValidationError, UserError



class AppointmentReport(models.AbstractModel):
    _name = 'report.sales_compare_report.report_sales_compare_document'
    _description = 'Sales Compare Report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['product_ids']:
            products = self.env['purchase.order.line'].search([('product_id', 'in', data['form']['product_ids'])])
        else:
            products = self.env['purchase.order.line'].search([])
#         raise ValidationError('%s'%products)
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
        return {
            'doc_model': 'purchase.order.line',
            'products': products,
        }