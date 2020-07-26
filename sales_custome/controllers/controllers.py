# -*- coding: utf-8 -*-
from odoo import http

# class SalesCustome(http.Controller):
#     @http.route('/sales_custome/sales_custome/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_custome/sales_custome/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_custome.listing', {
#             'root': '/sales_custome/sales_custome',
#             'objects': http.request.env['sales_custome.sales_custome'].search([]),
#         })

#     @http.route('/sales_custome/sales_custome/objects/<model("sales_custome.sales_custome"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_custome.object', {
#             'object': obj
#         })