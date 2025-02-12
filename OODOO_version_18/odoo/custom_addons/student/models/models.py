from odoo import models, fields

class Student(models.Model):
    _name = "student"  # Correct model name format
    _description = "Student Model"

    name = fields.Char(string="Student Name", required=True)
    roll = fields.Integer(int="Age")
    email = fields.Char(string="Email")
    address = fields.Text(string="Student's address",help="Enter student's permanent address here")
    html_field_demo = fields.Html(string="HTML Field Demo")
    is_agreed = fields.Boolean(string="Do you agree to the terms and consitons?", default="False", help="check to agree with the terms and conditions or else leave it un-checked")
    gender = fields.Selection(
        [("Male","Male"),("Female","Female")]
        )
    major = fields.Selection("_get_major_list", string="Select Major")

    def _get_major_list(self):
        return [("CS","Computer Science"),("IT","Information Technology"),("EC","Electronics and Communication"),("ME","Mechanical Engineering"), ("DA","Data Science and Artificial Engineering")]
