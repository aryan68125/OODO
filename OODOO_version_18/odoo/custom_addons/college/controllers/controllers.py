# -*- coding: utf-8 -*-
# from odoo import http


# class College(http.Controller):
#     @http.route('/college/college', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/college/college/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('college.listing', {
#             'root': '/college/college',
#             'objects': http.request.env['college.college'].search([]),
#         })

#     @http.route('/college/college/objects/<model("college.college"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('college.object', {
#             'object': obj
#         })

