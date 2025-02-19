# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class college(models.Model):
#     _name = 'college.college'
#     _description = 'college.college'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import api, models, fields
class College(models.Model):
    _name = "college"
    _description = "College Model"

    name = fields.Char(string = "College name")
    address = fields.Text(string = "Address")

