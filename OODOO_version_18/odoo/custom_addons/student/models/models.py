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
    # student_list = fields.One2many(comodel_name="student",inverse_name="school_id",required=False)
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
            ("school_id.name", "ilike", "stell"),
        ])
        print(f"Join table using any \n {students}")

        #  or operator
        students = self.env["student"].search([
            ("name", "!=", False),
            ("roll", "=", False)
        ])
        self.print_table(records=students)

        # select id,name from student where id > 4
        total_records = self.env["student"].search_count([("id",">","4")],limit=10)
        print("'select id,name from student where id > 4' ===> ",total_records)

        # search_count()
        print(f"search_count ===> {total_records}")

        # read_method()
        """
        Read method usage
        get data from a specific model.
        """
        print(f"read() ===> \n {self.read()}")
        print(f"read('name','gender') ===> \n {self.read(['name', 'gender'])}")

        # read_group() how to use it in odoo
        print(f"read_group() ===> {self.env["student"].read_group(domain=[], fields=['gender'], groupby=['gender'])}")
        student_group_by = self.env["student"].read_group([],['school_id'], ['school_id'])
        print("Student group by school_id ===> \n ")
        for student in student_group_by:
            print(f"{student}")
        """
        If you use 
        ```
            self.env["student"].read_group([],["school_id","gender"],["school_id","gender"])
            here by default lazy=True
        ```
        In this case it will give you the result for the first parameter "School_id" but it will not give you the result in case of "gender"
        {'school_id': (1, 'Stella Maris School'), 'school_id_count': 4, '__domain': [('school_id', '=', 1)], '__context': {'group_by': ['gender']}}
        {'school_id': (2, 'Lamartinier School'), 'school_id_count': 3, '__domain': [('school_id', '=', 2)], '__context': {'group_by': ['gender']}}
        {'school_id': (3, 'Delhi public school'), 'school_id_count': 1, '__domain': [('school_id', '=', 3)], '__context': {'group_by': ['gender']}}
        {'school_id': (5, 'Berlin School of Learning'), 'school_id_count': 2, '__domain': [('school_id', '=', 5)], '__context': {'group_by': ['gender']}}
        """
        student_group_by_gender = self.env["student"].read_group([],["school_id","gender"],["school_id","gender"])
        print(f"Student group by gender and school_id ===> \n")
        for student in student_group_by_gender:
            print(f"{student}")
        """
        If you use 
        ```
            self.env["student"].read_group([],["school_id","gender"],["school_id","gender"],lazy=True)
            here I have set lazy=False
        ```
        In this case it will give you the result for the first parameter "School_id" but it will not give you the result in case of "gender"
        {'school_id': (1, 'Stella Maris School'), 'school_id_count': 4, '__domain': [('school_id', '=', 1)], '__context': {'group_by': ['gender']}}
        {'school_id': (2, 'Lamartinier School'), 'school_id_count': 3, '__domain': [('school_id', '=', 2)], '__context': {'group_by': ['gender']}}
        {'school_id': (3, 'Delhi public school'), 'school_id_count': 1, '__domain': [('school_id', '=', 3)], '__context': {'group_by': ['gender']}}
        {'school_id': (5, 'Berlin School of Learning'), 'school_id_count': 2, '__domain': [('school_id', '=', 5)], '__context': {'group_by': ['gender']}}
        """
        student_group_by_gender = self.env["student"].read_group([],["school_id","gender"],["school_id","gender"],lazy=False)
        print(f"Student group by gender and school_id where lazy = False ===> \n")
        for student in student_group_by_gender:
            print(f"{student}")
        """
        student_order_by_fees ===> 
        [{'fees': 100.0, '__count': 2, '__domain': [('fees', '=', 100.0)]}, {'fees': 117.0, '__count': 1, '__domain': [('fees', '=', 117.0)]}, {'fees': 360.0, '__count': 1, '__domain': [('fees', '=', 360.0)]}, {'fees': 1000.0, '__count': 1, '__domain': [('fees', '=', 1000.0)]}, {'fees': 3000.0, '__count': 2, '__domain': [('fees', '=', 3000.0)]}, {'fees': 4000.0, '__count': 1, '__domain': [('fees', '=', 4000.0)]}, {'fees': 5000.0, '__count': 1, '__domain': [('fees', '=', 5000.0)]}, {'fees': 36500.0, '__count': 1, '__domain': [('fees', '=', 36500.0)]}]
        """
        student_order_by_fees = self.env["student"].read_group([],["fees"],["fees"],orderby="fees",lazy=False)
        print(f"student_fees order by fees ===> \n {student_order_by_fees}")

        # aggregation function sum, average : (by [day, month, count])
        """
        Calculate the average of all the fees os student
        student_average_fees ===> 
        [{'__count': 10, 'fees': 5317.7, '__domain': []}]
        """
        student_average_fees = self.env["student"].read_group(domain=[], fields=["fees:avg"], groupby=[], lazy=False)
        print(f"student_average_fees ===> \n {student_average_fees}")
        """
        Calculate the total sum of the fees
        total_fees_collected ===> 
        [{'__count': 10, 'fees': 53177.0, '__domain': []}]
        """
        total_fees_collected = self.env["student"].read_group(domain=[],fields=["fees:sum"],groupby=[],lazy=False)
        print(f"total_fees_collected ===> \n {total_fees_collected}")
        """
        total fees lax
        """
        total_fees_max = self.env["student"].read_group(domain=[],fields=["fees:max"],groupby=[],lazy=False)
        print(f"total_fees_max ===> \n {total_fees_max}")

        # search_read method
        """
        search method returns the record set and read method returns the list of dictionaries for that specific record.
        SELECT * FROM student where id=1 --> This ** where ** condition is what you have to pass in the domain

        if load = None then the display name of many2one field is not shown
        search_read( domain , fields [id, name, student_id], offset=type(int), limit=type(int), order,load=None,)
        """
        """
        student_search_read ===> 
        [{'id': 9, 'name': 'Shotgun'}, {'id': 11, 'name': 'Recon'}, {'id': 7, 'name': 'Barbatos'}, {'id': 8, 'name': 'ShockWave'}, {'id': 1, 'name': 'Rollex997'}, {'id': 5, 'name': 'Ignition'}, {'id': 4, 'name': 'Bullet'}, {'id': 2, 'name': 'Ballistic'}, {'id': 3, 'name': 'Barricade'}, {'id': 6, 'name': 'Kombat'}, {'id': 20, 'name': 'Artillery'}]
        """
        student_search_read = self.env["student"].search_read(domain=[],fields=["id","name","school_id"],order="fees")
        print(f"student_search_read ===> \n {student_search_read}")

        """
        student_search_read_with_domain where school_id = 1 ===> 
        [{'id': 9, 'name': 'Shotgun', 'school_id': (1, 'Stella Maris School')}, {'id': 7, 'name': 'Barbatos', 'school_id': (1, 'Stella Maris School')}, {'id': 8, 'name': 'ShockWave', 'school_id': (1, 'Stella Maris School')}, {'id': 1, 'name': 'Rollex997', 'school_id': (1, 'Stella Maris School')}]
        """
        student_search_read_with_domain = self.env["student"].search_read(domain=[("school_id","=",1)],fields=["id","name","school_id"],order="fees",limit=2)
        print(f"student_search_read_with_domain where school_id = 1 ===> \n {student_search_read_with_domain}")

    # name_create method
    @api.model
    def name_create(self,name):
        print(f"name_create method : ",self,name)
        result = super(School,self).name_create(name)
        print(f"name_create method result ==> {result}")
        return result
    
    # default_get method
    @api.model
    def default_get(self,fields_list):
        print(f" Default get method ",self,fields_list)
        result = super(School,self).default_get(fields_list)
        print(f"result ===> {result}")
        return result

    def print_location(self,records):
        print(f"Total Record Found :- {len(records)}")
        print(f"ID                  NAME            PARENT")
        for rec in records:
            print(f"{rec.id}        {rec.name}         {rec.parent_id.name} / {rec.parent_id.id}")
        




