# -*- coding: utf-8 -*-
# from odoo import http


# class Marks(http.Controller):
#     @http.route('/marks/marks', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marks/marks/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('marks.listing', {
#             'root': '/marks/marks',
#             'objects': http.request.env['marks.marks'].search([]),
#         })

#     @http.route('/marks/marks/objects/<model("marks.marks"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marks.object', {
#             'object': obj
#         })

