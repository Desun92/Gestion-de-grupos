# -*- coding: utf-8 -*-
# from odoo import http


# class GestionDeGrupos(http.Controller):
#     @http.route('/gestion_de_grupos/gestion_de_grupos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_de_grupos/gestion_de_grupos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_de_grupos.listing', {
#             'root': '/gestion_de_grupos/gestion_de_grupos',
#             'objects': http.request.env['gestion_de_grupos.gestion_de_grupos'].search([]),
#         })

#     @http.route('/gestion_de_grupos/gestion_de_grupos/objects/<model("gestion_de_grupos.gestion_de_grupos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_de_grupos.object', {
#             'object': obj
#         })
