from odoo import models, fields

class Student(models.Model):
    _name = "student"  # Correct model name format
    _description = "Student Model"

    name = fields.Char(string="Student Name", required=True)
    roll = fields.Integer(int="Age")
    email = fields.Char(string="Email")
    address = fields.Text(string="Student's address",help="Enter student's permanent address here")
