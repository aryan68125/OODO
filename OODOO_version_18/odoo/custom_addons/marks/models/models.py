# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class marks(models.Model):
#     _name = 'marks.marks'
#     _description = 'marks.marks'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

# from odoo import models, fields, api

# class Marks(models.Model):
#     _name = 'marks'
#     _description = 'Student Marks'

#     subject_name = fields.Char(string="Subject name", required=True, index=True)
#     marks = fields.Integer(string="Marks",default=0, copy=False)
#     grade = fields.Char(string="Student's grade",compute="_compute_grade", required=False)
#     student_name = fields.Char(string="Student Name", required=True,readonly=False,translate=True)

#     @api.depends('marks')
#     def _compute_grade(self):
#         for record in self:
#             if record.marks >=91 and record.marks <= 100:
#                 record.grade = "A+"
#             elif record.marks >=81 and record.marks <= 90:
#                 record.grade = "A"
#             elif record.marks >=71 and record.marks <= 80:
#                 record.grade = "B"
#             elif record.marks >=61 and record.marks <= 70:
#                 record.grade = "C"
#             elif record.marks >=51 and record.marks <= 60:
#                 record.grade = "D"
#             elif record.marks >=41 and record.marks <= 50:
#                 record.grade = "E"
#             else:
#                 record.grade = "F"

from odoo import models, fields, api

class Marks(models.Model):
    _name = 'marks'
    _description = 'Student Marks'

    subject_name = fields.Char(string="Subject name")
    marks = fields.Integer(string="Marks")
    grade = fields.Char(string="Student's grade",compute="_compute_grade")
    student_name = fields.Char(string="Student Name")

    @api.depends('marks')
    def _compute_grade(self):
        for record in self:
            if record.marks >=91 and record.marks <= 100:
                record.grade = "A+"
            elif record.marks >=81 and record.marks <= 90:
                record.grade = "A"
            elif record.marks >=71 and record.marks <= 80:
                record.grade = "B"
            elif record.marks >=61 and record.marks <= 70:
                record.grade = "C"
            elif record.marks >=51 and record.marks <= 60:
                record.grade = "D"
            elif record.marks >=41 and record.marks <= 50:
                record.grade = "E"
            else:
                record.grade = "F"
