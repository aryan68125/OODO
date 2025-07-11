from odoo import api, models, fields
from datetime import date
from odoo.exceptions import ValidationError
class School(models.Model):
    # model meta-data
    _name = "school"
    _description = "Student School"
    # model fields
    name = fields.Char(string="Student's School",required=True)
    ref_field_id = fields.Reference(selection=[('hobby','Hobby'),('student','Student')], string="Reference field demo")
    student_list = fields.One2many(comodel_name="student",inverse_name="school_id")
    address = fields.Char(string="School address")
    @api.constrains('student_list')
    def _check_student_list_not_empty(self):
        for record in self:
            if not record.student_list:
                raise ValidationError("You must add at least one student.")


class Hobby(models.Model):
    # model meta-data
    _name = "hobby"
    _description = "Student Hobby"
    # model fields
    name = fields.Char(string = "Hobby Name")
    
    """
    A custom model to demonstrate the use of a button in the form view.
    This model is used to create a button in the form view of the hobby model.
    The button will call a custom method in the hobby model when clicked.
    The custom method will create a new hobby records in the hobby model.
    """
    # def custom_method(self):
    #     print("clicked! custom method in the hobby model called!")
    #     data = {"name":"Archery"}
    #     self.env["hobby"].create(data)
    """A custom method to demonstrate the use of a button in the form view.
    This method is called when the button is clicked in the form view of the hobby model.
    This method will create 4 new hobby records in the hobby model.
    """
    # def custom_method(self):
    #     print("clicked! custom method in the hobby model called!")
    #     data = [
    #         {"name":"Hunting down naxals"},
    #         {"name":"Researching for Ai"},
    #         {"name":"Axe throwing"},
    #         {"name":"Archery"}
    #     ]
    #     self.env["hobby"].create(data)

    """
    A custom method to demonstrate the use of a button to update a single record in the hobby model.
    """
    def custom_method(self):
        print(f"clicked! custom method will update a record in the hobby model")
        print(f"self ===> {self}")
        # update the first record in the hobby model with a new name
        # self.env["hobby"].search([('id', '=', 1)], limit=1).write({"name":"Killing terrorists"})
        # update the first record in the hobby model with a new name 
        self.env["hobby"].browse(1).write({"name":"Killing porkistani terrorists"})


class Student(models.Model):
    # model meta-data
    _name = "student"  # Correct model name format
    _description = "Student Model"
    # model fields
    profile_picture = fields.Image("Student's profile picture")
    school_id = fields.Many2one(comodel_name = 'school', string="Select Student's School",help="Select student's school", default=1)
    school_address = fields.Char(related='school_id.address', string="School address", store=True)
    hobby_list = fields.Many2many(comodel_name="hobby",relation="student_hobby_list_relation",column1="student_id",column2="hobby_id")
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
    
    # compute method
    @api.depends('name')
    def compute_added_at(self):
        self.added_at = date.today()

    # override the create method
    # METHOD 1 : without using any decorators
    # def create(self,vals):
    #     print(f"vals in the create method for the Surtend model ===> {vals}")
    #     # super will automatically return the record created by the create method
    #     result = super(Student ,self).create(vals)
    #     print(f"result in the create method for the Student model ===> {result}")
    #     return result
    # METHOD 2 : using decorators using @api.model decorator
    # @api.model
    # def create(self, vals):
    #     print(f"create method using an api.model decorator")
    #     print(f"vals in the create method for the Student model ===> {vals}")
    #     # super will automatically return the record created by the create method
    #     result = super(Student, self).create(vals)
    #     print(f"result in the create method for the Student model ===> {result}")
    #     return result
    # METHOD 2 : using decorators @api.model_create_multi decorator
    # @api.model_create_multi
    # def create(self, vals):
    #     print(f"create method using an api.model_create_multi decorator")
    #     print(f"vals in the create method for the Student model ===> {vals}")
    #     # super will automatically return the record created by the create method
    #     result = super(Student, self).create(vals)
    #     print(f"result in the create method for the Student model ===> {result}")
    #     return result
    # METHOD 2 : using decorators @api.model_create_multi decorator
    @api.model_create_multi
    def create(self, vals_list):
        print(f"create method using an api.model_create_multi decorator")
        print(f"vals in the create method for the Student model ===> {vals_list}")
        # super will automatically return the record created by the create method
        result = super().create(vals_list)
        print(f"result in the create method for the Student model ===> {result}")
        return result
    
    """
    override the write method
    """
    def write(self,vals):
        print(f"write method called for the Student model with vals ===> {vals}")
        # super will automatically return the record updated by the write method
        result = super(Student, self).write(vals)
        print(f"result in the write method for the Student model ===> {result}")
        # the return type is boolean 
        return result
    
    """
    custom method that mimics the functionality of copy method the duplicate button in the form view
    """
    def duplicate_records(self):
        print(f"self ===> {self}") 
        duplicate_data = self.copy()
        print(f"duplicated_data ===> {duplicate_data}")

    """
    override copy method to duplicate records
    This method will not copy the data in those field when creating a duplicate record where it has the attribute `copy=False`
    """
    @api.returns('self', lambda value: value.id)
    def copy(self,default=None):
        print(f"self ===> {self}")
        print(f"default ===> {default}")
        return_data = super(Student,self).copy(default=default)
        print(f"return_data from copy method ===> {return_data}")
        return return_data
    
    """
    Use custom method to delete a record using our own button in the front-end side of the odoo
    """
    def delete_record(self):
        print(f"self delete_record method ===> {self}")
        result = self.unlink()
        print(f"Record deleted success status ===> {result}")
    """
    override unlink method to delete records
    """
    def unlink(self):
        print(f"self unlink method ===> {self}")
        # super will automatically return the record deleted by the unlink method
        result = super(Student, self).unlink()
        print(f"result in the unlink method for the Student model ===> {result}")
        # the return type is boolean 
        return result
    
    """
    custom search method. 
    """
    def print_table(self, records):
        for rec in records:
            print(f"Student: {rec.name}, Fees: {rec.fees}")
    def search_record(self):
        # print self method
        print(f"self search_record method ===> {self}")

        # search(domain, limit, offset, order)
        # [condition, more conditions]
        
        print(f"search_record return student recordset ===> {self.env['student'].search([])}")
        print(f"search_record return school recordset ===> {self.env["school"].search([])}")
        # self.search([("name","ilike","web")]) ===> domain = [("name","ilike","web")]  ===> domain conditions
        print(f"search_record return student recordset domain conditions ('name','ilike','web') ===> {self.search([("name","ilike","rol")])}")
        # if you want to apply a limit
        print(f"search_record return student recordset using limit ===> {self.search([("name","ilike","rol")], limit=5)}")
        # if you want to apply offset
        print(f"search_record return student recordset using limit on gender field ===> {self.search([("gender","ilike","Male")], limit=5)}")
        print(f"search_record return student recordset using limit and offset on gender field ===> {self.search([("gender","ilike","Male")], limit=5,offset=1)}")
        # order by
        print(f"search_record return student recordset order by on name ===> {self.search([],order="name")}")
        print(f"search_record return student recordset order by on id desc ===> {self.search([],order="id desc")}")
        # apply sql where condition in odoo
        print(f"where condition in search ===> {self.search([("fees","=",4000)])}")
        self.print_table(self.search([("fees","=",4000)]))
        print(f"I want to get all the records that are grater than 100")
        self.print_table(self.search([("fees",">",100)]))
        # where clause in operator.
        print(f"check multiple records using where clause in a record set")
        self.print_table(self.search([("fees","!=",(4000,100,5000,1000))]))

        # IN
        print(f"in operator demo ===> {self.search([("fees", "in", (100, 4000))])}")
        # NOT IN
        print(f"not in operator demo ===> {self.search([("fees", "not in", (100, 4000))])}")
        # LIKE
        print(f"like operator demo ===> {self.search([("name", "like", "Ba")])}")
        # NOT LIKE
        print(f"not like in operator demo ===> {self.search([("name", "not like", "Ro")])}")
        # ILIKE
        print(f"ilike in operator demo ===> {self.search([("name", "ilike", "Ba")])}")
        # NOT ILIKE
        print(f"not ilike in operator demo ===> {self.search([("name", "not ilike", "Ba")])}")
        # =ilike
        print(f"=ilike operator ===> {self.search([("name","=like","%Ro%")])}")

        # child_of
        print(f"search_record return student recordset ===> {self.env['student'].search([])}")

        parent_hobby = self.env['hobby'].search([('name', '=', 'Music')], limit=1)
        descendants = self.env['hobby'].search([('id', 'child_of', parent_hobby.id)])
        print(f"Parent hobby table \n")
        self.print_location(parent_hobby)
        print(f"Descendants table \n")
        self.print_location(descendants)

        # join Query
        # any
        students = self.env["student"].search([
            ("student_fee_ids.amount", "=", 0),
            ("student_fee_ids.name", "ilike", "web")
        ])
        print(f"Join table using any {students}")

    def print_location(self,records):
        print(f"Total Record Found :- {len(records)}")
        print(f"ID                  NAME            PARENT")
        for rec in records:
            print(f"{rec.id}        {rec.name}         {rec.parent_id.name} / {rec.parent_id.id}")
        




