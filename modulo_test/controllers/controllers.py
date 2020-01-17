# -*- coding: utf-8 -*-
from odoo import http

# class ModuloTest(http.Controller):
#     @http.route('/modulo_test/modulo_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_test/modulo_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_test.listing', {
#             'root': '/modulo_test/modulo_test',
#             'objects': http.request.env['modulo_test.modulo_test'].search([]),
#         })

#     @http.route('/modulo_test/modulo_test/objects/<model("modulo_test.modulo_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_test.object', {
#             'object': obj
#         })