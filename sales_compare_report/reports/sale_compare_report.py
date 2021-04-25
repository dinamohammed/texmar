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
            purchase_lines = self.env['purchase.order.line'].search(
                [('product_id','in',data['form']['product_ids'])],order='product_id')
        else:
            purchase_lines = self.env['purchase.order.line'].search([])
        ###### call function to update product values: Market Gallery Dealer
        self.env['product.product']._get_total_values_current_year()
        self.env['product.product']._get_total_values_last_year()

        return {
            'doc_model': 'purchase.order.line',
            'purchase_lines': purchase_lines,
            'products': products,
        }