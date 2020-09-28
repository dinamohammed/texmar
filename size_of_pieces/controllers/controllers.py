# -*- coding: utf-8 -*-
# from odoo import http


# class SizeOfPieces(http.Controller):
#     @http.route('/size_of_pieces/size_of_pieces/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/size_of_pieces/size_of_pieces/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('size_of_pieces.listing', {
#             'root': '/size_of_pieces/size_of_pieces',
#             'objects': http.request.env['size_of_pieces.size_of_pieces'].search([]),
#         })

#     @http.route('/size_of_pieces/size_of_pieces/objects/<model("size_of_pieces.size_of_pieces"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('size_of_pieces.object', {
#             'object': obj
#         })
