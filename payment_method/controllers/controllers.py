# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentMethod(http.Controller):
#     @http.route('/payment_method/payment_method/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_method/payment_method/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_method.listing', {
#             'root': '/payment_method/payment_method',
#             'objects': http.request.env['payment_method.payment_method'].search([]),
#         })

#     @http.route('/payment_method/payment_method/objects/<model("payment_method.payment_method"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_method.object', {
#             'object': obj
#         })
