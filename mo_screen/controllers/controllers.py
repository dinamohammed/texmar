# -*- coding: utf-8 -*-
# from odoo import http


# class MoScreen(http.Controller):
#     @http.route('/mo_screen/mo_screen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mo_screen/mo_screen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mo_screen.listing', {
#             'root': '/mo_screen/mo_screen',
#             'objects': http.request.env['mo_screen.mo_screen'].search([]),
#         })

#     @http.route('/mo_screen/mo_screen/objects/<model("mo_screen.mo_screen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mo_screen.object', {
#             'object': obj
#         })
