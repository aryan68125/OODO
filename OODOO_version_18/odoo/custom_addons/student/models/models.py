from odoo import api, models, fields
from datetime import date

class School(models.Model):
    _name = "school"
    _description = "Student School"
    name = fields.Char(string="Student's School",required=True)
    student_list = fields.One2many("student","school_id")
    ref_field_id = fields.Reference([('hobby','Hobby'),('student','Student')])
class Hobby(models.Model):
    _name = "hobby"
    _description = "Student Hobby"
    name = fields.Char(string = "Hobby Name")
class Student(models.Model):
    _name = "student"  # Correct model name format
    _description = "Student Model"

    school_id = fields.Many2one(comodel_name = 'school', string="Select Student's School",help="Select student's school", default=1)
    hobby_list = fields.Many2many("hobby","student_hobby_list_relation","student_id","hobby_id")
    name = fields.Char(string="Student Name", required=True)
    roll = fields.Integer(int="Age")
    email = fields.Char(string="Email")
    address = fields.Text(string="Student's address",help="Enter student's permanent address here") 
    html_field_demo = fields.Html(string="HTML Field Demo")
    is_agreed = fields.Boolean(string="Do you agree to the terms and consitons?", default="False", help="check to agree with the terms and conditions or else leave it un-checked")
    fees = fields.Float(string="Student's Fees",digits=(4,4))
    school_data = fields.Json(string="School Data")
    # joining_date = fields.Date(string="Joining Date",default="2025-02-16")
    # joining_date = fields.Date(string="Joining Date")
    joining_date = fields.Datetime(string="Joining Date",default=fields.Datetime.now)
    added_at = fields.Date(string="Added at",compute="compute_added_at")

    '''
    The ways to implement selection fields in odoo are:
    '''
    '''
    Method 1:
    '''
    gender = fields.Selection(
        selection = [("Male","Male"),("Female","Female")]
        )
    '''
    Method 2:
    '''
    major = fields.Selection(selection = "_get_major_list", string="Select Major")
    def _get_major_list(self):
        return [("CS","Computer Science"),("IT","Information Technology"),("EC","Electronics and Communication"),("ME","Mechanical Engineering"), ("DA","Data Science and Artificial Engineering")]

    def json_data_store(self):
        self.school_data = {'name':self.name, 'roll_no':self.roll}
    
    @api.depends('name')
    def compute_added_at(self):
        self.added_at = date.today()
