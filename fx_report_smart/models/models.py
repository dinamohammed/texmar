# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FxReport(models.Model):
    _name = 'fx.report.smart'
#     _description = 'fx_report_smart.fx_report_smart'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
