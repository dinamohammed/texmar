# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class payment_receipt_report(models.Model):
#     _name = 'payment_receipt_report.payment_receipt_report'
#     _description = 'payment_receipt_report.payment_receipt_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
