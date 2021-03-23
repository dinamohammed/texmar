# -*- coding: utf-8 -*-
import base64
import io

import math

from odoo import models


class SaleCompareXlsx(models.AbstractModel):
    _name = 'report.sales_compare_report.report_sales_compare_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoice_ids):
        report_name = "Sales Compare Report"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name)
        format_left_to_right = workbook.add_format()
        format_left_to_right.set_reading_order(1)
        
#         format_right_to_left = workbook.add_format()
#         format_right_to_left.set_reading_order(2)
#         cell_format_right = workbook.add_format()
#         cell_format_right.set_align('right')
        
#         worksheet.left_to_right()
        
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:F', 10)
        worksheet.set_column('G:J', 5)
        worksheet.set_column('K:L', 10)
        worksheet.set_column('M:T', 10)
        worksheet.set_column('U:U', 15)
        
        
        bold = workbook.add_format({'bold': True})
        bold.set_font_size(12)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(15)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(12)
        bold_left = workbook.add_format({'bold': True, 'align': 'left'})
        bold_left.set_font_size(12)
        
        row = 0
        worksheet.merge_range(row, 0, row, 20, "PREPARATION", bold_center)
        
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        
        ########################## Table header ########################
        row += 1
        col = 0
        
        worksheet.merge_range(row, col, row+1, col, 'Ser', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Code', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Name', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Color', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Delivery Date', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Qty', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col+5, 'PO', cell_format_header)
        col += 6
        worksheet.merge_range(row, col, row, col+2, 'Current Year', cell_format_header)
        worksheet.write(row+1, col, 'Gallery', cell_format_header)
        col += 1
        worksheet.write(row+1, col, 'Dealer', cell_format_header)
        col += 1
        worksheet.write(row+1, col, 'Market', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row, col+2, 'Last Year', cell_format_header)
        worksheet.write(row+1, col, 'Gallery', cell_format_header)
        col += 1
        worksheet.write(row+1, col, 'Dealer', cell_format_header)
        col += 1
        worksheet.write(row+1, col, 'Market', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Total', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'Request', cell_format_header)
        col += 1
        worksheet.merge_range(row, col, row+1, col, 'PO Qty', cell_format_header)
        col += 1