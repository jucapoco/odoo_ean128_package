# -*- coding: utf-8 -*-
from openerp import http

# class Ean128Package(http.Controller):
#     @http.route('/ean128_package/ean128_package/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ean128_package/ean128_package/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ean128_package.listing', {
#             'root': '/ean128_package/ean128_package',
#             'objects': http.request.env['ean128_package.ean128_package'].search([]),
#         })

#     @http.route('/ean128_package/ean128_package/objects/<model("ean128_package.ean128_package"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ean128_package.object', {
#             'object': obj
#         })