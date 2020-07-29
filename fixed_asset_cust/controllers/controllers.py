# -*- coding: utf-8 -*-
# from odoo import http


# class FixedAssetCust(http.Controller):
#     @http.route('/fixed_asset_cust/fixed_asset_cust/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fixed_asset_cust/fixed_asset_cust/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fixed_asset_cust.listing', {
#             'root': '/fixed_asset_cust/fixed_asset_cust',
#             'objects': http.request.env['fixed_asset_cust.fixed_asset_cust'].search([]),
#         })

#     @http.route('/fixed_asset_cust/fixed_asset_cust/objects/<model("fixed_asset_cust.fixed_asset_cust"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fixed_asset_cust.object', {
#             'object': obj
#         })
