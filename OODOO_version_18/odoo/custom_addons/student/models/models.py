from odoo import api, models, fields
from datetime import date
from odoo.exceptions import ValidationError
from lxml import etree

import logging 
_logger = logging.getLogger("Aditya's custom logger :-")

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

class Curreny(models.Model):
    _name = "student_currency"
    _description = "Student Currency"
    name = fields.Char(string="Student Currency", required=False)
    # Override the name search method in odoo models 
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        print(f"_name_search called on student_currency. Search term: {name}")
        domain = domain or []
        if name:
            domain += [('name', operator, name)]
        result = self._search(domain, limit=limit, order=order)
        print(f"Result IDs: {result}")
        return self.browse(result).name_get()
    
class Student(models.Model):
    # model meta-data
    _name = "student"  # Correct model name format
    _description = "Student Model"
    # model fields
    # to make model soft delete instead of hard delete
    active = fields.Boolean(string="Archive / Soft delete / Remove from filter",default=True)
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
    currency = fields.Many2one(comodel_name = "student_currency",string = "Select student's currency", help="Select student's school", default=1)
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

        """
        search the archived fields in odoo
        """
        archived_student_search = self.env["student"].search_read(domain = [("active","=",False)])
        print(f"archived_student_search ===> {len(archived_student_search)}")

    # name_create method
    @api.model
    def name_create(self,name):
        print(f"name_create method : ",self,name)
        result = super(School,self).name_create(name)
        print(f"name_create method result ==> {result}")
        return result
    
    # default_get method
    # @api.model
    # def default_get(self,fields_list):
    #     print(f" Default get method ",self,fields_list)
    #     result = super(School,self).default_get(fields_list)
    #     print(f"result ===> {result}")
    #     return result

    def print_location(self,records):
        print(f"Total Record Found :- {len(records)}")
        print(f"ID                  NAME            PARENT")
        for rec in records:
            print(f"{rec.id}        {rec.name}         {rec.parent_id.name} / {rec.parent_id.id}")

    """
    This method is called as soon as the page is loaded on the browser.
    
    get_view returns an architecture in xml format. 
    We have to parse this xml data for this we will be needing lxml library

    This method can be used to change the field positions in the form view of the student model. 
    """
    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        # print(f"get_view ===> view_id={view_id}, view_type={view_type}, options={options}")
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form" and "arch" in result:
            doc = etree.fromstring(result["arch"])
            # print(f"doc ===> \n {doc}")
            # targetted field
            school_field = etree.Element("field",{"name":"school_id"})
            targeted_field = doc.xpath("//field[@name='name']")
            if targeted_field:
                """ In the form view of the student the Select Student's School field will be displayed after Student's name """
                # targeted_field[0].addnext(school_field)
                """ In the form view of the student the select Student's school field will be displayed before the student's name """
                targeted_field[0].addprevious(school_field)
            # again we need to convert this doc object into the string
            result["arch"] = etree.tostring(doc,encoding="unicode")
            # print(f"get_view :: result ===> \n {result}")
        return result

    """
    Demonstration of sub_custom_method along with self.ensure_one() method
    """
    # def sub_custom_method(self):
    #     print(f"Sub custom method !!!!")
    #     """
    #     It uses self.ensure_one() to ensure only one record is being operated upon.
    #     This is an Odoo utility method that raises an error if self (the recordset) contains more than one record.

    #     If a blank or more than one recordset is found then it will throw an error!
    #     """
    #     self.ensure_one()
    #     print(self)
    #     print(f"printing student name in sub custom method >>> ")
    #     print(self.name)

    # def custom_method(self):
    #     print("Custom method clicked !!!")
    #     print(self)
    #     # Here get school from the self.search([]) and then print school.sub_custom_method() inside the loop
    #     for school in self.search([]):
    #         school.sub_custom_method()
    #         print(f"school.sub_custom_method() ===> {school.sub_custom_method()}")
    #     print(f"sub_custom_method called from custom_method !!!")
    #     self.sub_custom_method()

    """
    Demo of how filter method works in odoo.
    """
    # def custom_method(self):
    #     print(f"custom method clicked!!!")
    #     print(f"self ===> {self}")
    #     """
    #     Everytime you call search method odoo will hit the database.
    #     If suppose there is a senario where data must be filtered multiple times from the recordset where we want to reduce the number of hits to the database
    #     in that case we will have to use filter method.
    #     """
    #     students = self.env["student"].search([])
    #     print(f"students ===> {students}")
    #     student_filtered = self.env["student"].search([("name","ilike","rollex")])
    #     print(f'("name","ilike","ddd") ===> {student_filtered.name}')

    #     """filter method demonstration"""
    #     # Case 1 where search method and domain search is used to get the student using their names
    #     student_filtered = self.env["student"].search([("name","ilike","rollex")])
    #     print(f'("name","ilike","ddd") ===> {student_filtered.name}')

    #     # Case 2 where the student is searched using student.ids and names in the domain 
    #     student_filtered = self.env["student"].search([("id","in",students.ids),("name","ilike","balli")])
    #     print(f'("id","in",students.ids),("name","ilike","ddd")  ===> {student_filtered.name}')

    #     # Case 3 where I want to find the student name that starts like "Ba" :: without filter method
    #     stud_obj = self.env["student"]
    #     for stud in students:
    #         if "Ro" in str(stud.name):
    #             stud_obj += stud 
    #     print(f"stud_obj without using filtered ===> {stud_obj}")

    #     # Case 4 where I want to find the student name that starts like "Ba" :: with filter method
    #     """
    #     Here the filtered method won't be making any calls to the database.
    #     It filters the data from the existing queryset and only shows the results that matches the condition.
    #     """
    #     stud_obj = students.filtered(lambda stud: "Ba" in str(stud.name))
    #     print(f"stud_obj using filtered ===> {stud_obj}")


    """
    Demo of mapped method in odoo
    """
    # def custom_method(self):
    #     print(f"custom method with the demo of mapped method called!!")
    #     print(self)
    #     student_obj = self.env["student"]
    #     student_ids = student_obj.search([])
    #     print(f"Here school_id is a recordset ===> ")
    #     print(f"student_ids ===> {student_ids}")

    #     student_fees = []

    #     # case 1 : what you will have to do if you don't use mapped
    #     for student in student_ids:
    #         student_fees.append(student.fees)
    #     print(f"student_fees using for loop ===> {student_fees}")
    #     print(f"Total fees collected ===> {sum(student_fees)}")

    #     # case 2 : The same logic that is used to calcualte the sum of all the fees of students using mapped method()
    #     """
    #     Mapped method in odoo is a shortcut to extract values from the fields or apply methods accross a record set
    #     It worked recursively and returns a list

    #     student_ids = self.env["student"].search([])
    #     # Get names of the school for each student
    #     school_names = student_ids.mapped("school_id.name")
    #     [It is equivalent to this]
    #     school_names = [student.school_id.name for student in student_ids]
    #     But .mapped() is more effitient , clean and readable.

    #     | Use Case                                                         | Example                                                                |
    #     | ---------------------------------------------------------------- | ---------------------------------------------------------------------- |
    #     | You want to **extract a field value** from multiple records      | `students.mapped("name")`                                              |
    #     | You want to **traverse relationships**                           | `students.mapped("school_id.name")`                                    |
    #     | You want to **combine values from related fields**               | `orders.mapped("order_line.product_id.name")`                          |
    #     | You want to call a **method on each record** and collect results | `students.mapped("custom_method")` (if `custom_method` returns values) |

    #     Inside the mapped method you need to specify the specific field that you want to map here in this case the mapped field is "fees"

    #     Returns of .mapped() method : 
    #     | Type of Field       | Return Type             |
    #     | ------------------- | ----------------------- |
    #     | Many2one            | Recordset or list       |
    #     | One2many            | Recordset               |
    #     | Char, Integer, etc. | List                    |
    #     | Method              | List (of return values) |

    #     """
    #     student_school_mapped = student_ids.mapped("school_id").mapped("name")
    #     print(f"student_school_mapped ===> {student_school_mapped}")

    """
    Demo of sorted() method
    """
    # def custom_method(self):
    #     print(f"Custom method with to demo sorted function is called !!!")
    #     students_recordset = self.env["student"].search([])
        
    #     """
    #     As you can see in this case the order by ascending and descending order is being applied on the recordset and everytime the order_by is called then a new recordset
    #     is created hence in this case database is being hit everytime.
    #     """
    #     # order by id in ascending order
    #     stud = students_recordset.search([],order="id")
    #     print(f"student in ascending order ===> {stud}")
        
    #     # order by id in descending order
    #     stud = students_recordset.search([],order="id desc")
    #     print(f"student in descending order ===> {stud}")

    #     """
    #     Sorted function
    #     """
    #     # ascending order
    #     stud_list = stud.sorted(key=lambda stud: stud.id)
    #     """
    #     NOTE : If you do this stud_list.name
    #     then you will get this error ValueError: Expected singleton: student(1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20)
    #     This error means that you trying to access a field from a list of recordset and odoo cannot get that field value because its a list you need to loop through that list
    #     and get each record to be able to even access that field value.
    #     If you want to avoid for loops then you can use mapped function with the field name inside double quotes.
    #     """
    #     print(f"stud_list using sorted function ===> \n {stud_list} \n {stud_list.mapped("name")}")

    #     # descending order
    #     stud_list = stud.sorted(key=lambda stud: stud.id,reverse=True)
    #     print(f"stud_list using sorted function ===> \n {stud_list} \n {stud_list.mapped("name")}")

    """
    How to use grouped function A different way to implement the functionality of a group_by function
    """
    # def custom_method(self):
    #     print(f"Custom method to demo the group_by function is clicked!")
    #     print(self)
    #     student_list = self.env["student"].search([])
    #     print(f"students list in the list of recordset ===> {student_list}")

    #     """
    #     Group by 
        
    #     If you want to group by records from an existing recordset then it is possible using the group function
    #     For example: 
    #     - If you want to get the group by from the recordset itself
    #     """
    #     student_grouped_list = student_list.grouped(key="major")
    #     print(f"student_grouped_list ===> {student_grouped_list}")

    """
    custom function to demonstrate the fields_get() function
    """
    # def custom_method(self):
    #     print(f"custom method clicked to demonstrate the fields_get() function")
    #     # print(self)
        
    #     students_object = self.env["student"].search([])
    #     # print(f"students_object ===> {students_object}")

    #     """
    #     students_object.fields_get()
    #     This will return all the field list and its meta data along with all of its attributes

    #     To view the generated result you can use online json viewer https://jsonviewer.stack.hu/
    #     """
    #     student_group_list = students_object.fields_get()
    #     # print(f"students_object.fields_get() ===> {student_group_list}")

    #     """
    #     students_object.fields_get(field_list, attributes)
    #     if field_list is given then only fields mentioned in the field list will be returned will all its attributes and its metadata
    #     """
    #     student_group_list = students_object.fields_get(["name","roll"])
    #     print(f"students_object.fields_get() field_list ===> {student_group_list}")

    """
    get_metadata method implementation in custom method
    """
    # def custom_method(self):
    #     print(f"custom method to demo the get_metadata method")
    #     print(f"self ===> {self}")
    #     print(f"{self.get_metadata()}")

    #     # Use for loop to display field's meta data
    #     for stud in self.env["student"].search([]):
    #         print(stud, " ",stud.name, " ",stud.get_metadata())

    """
    search_fetch method implementation in custom method ODOO 18 only
    before you do anything you need to 
    import logging 
    _logger = logging.getLogger()
    """
    # def custom_method(self):
    #     print(f"Custom method that demonstrates the search_fetch ")
    #     print(f" self ===> {self} ")

    #     """
    #     search_fetch method is the combination of search and the fetch method.

    #     fetch method doesn't return anything which is also and ORM method and it stores in the cache memory.
    #     This method is very similar to the search method as well as the read method

    #     search_fetch method is faster when compared to the search method.

    #     self.search_fetch([],["id","name]) this is not a read method that you will get id and the name but it will still return a recordset and using the fetch method only get "id" and "name" into the cache memory, It will update the cache memeory for these two fields.
    #     will be updated accordingly.
    #     """
    #     student_obj = self.search_fetch([],[])
    #     print(f"student_obj ===> {student_obj}")

    #     for student in student_obj:
    #         print(f"student_name ===> {student.name} :: student_school_name ===> {student.school_id.name} :: student_address ===> {student.school_id.address}")

    """
    custom method to demonstrate custom logs implementation in case of odoo server
    """
    # def custom_method(self):
    #     print(f"Custom method that demonstrates the custom_logs in odoo")
    #     """There are 5 different types of logs available"""
    #     student_obj = self.search_fetch([],[])

    #     for student in student_obj:
    #         _logger.info(f"student_name ===> {student.name} :: student_school_name ===> {student.school_id.name} :: student_address ===> {student.school_id.address}")

    """
    This custom method demonstrates odoo special commands
    """
    def custom_method(self):
        sale_order_vals = [{'locked': False, 'partner_id': 27, 'validity_date': '2025-09-04', 'date_order': '2025-08-05 10:46:58', 'show_update_pricelist': False, 'company_id': 1, 'pricelist_id': False, 'payment_term_id': 2, 'order_line': [[0, 'virtual_74', {'sequence': 10, 'display_type': False, 'is_downpayment': False, 'product_id': 32, 'product_template_id': 23, 'product_custom_attribute_value_ids': [[6, False, []]], 'product_no_variant_attribute_value_ids': [[6, False, []]], 'linked_line_id': False, 'virtual_id': False, 'linked_virtual_id': False, 'selected_combo_items': False, 'combo_item_id': False, 'name': '[FURN_6667] Acoustic Bloc Screens (Wood)', 'product_uom_qty': 1, 'product_uom': 1, 'customer_lead': 0, 'price_unit': 295, 'technical_price_unit': 295, 'tax_id': [], 'product_document_ids': []}], [0, 'virtual_83', {'sequence': 11, 'display_type': False, 'is_downpayment': False, 'product_id': 21, 'product_template_id': 15, 'product_custom_attribute_value_ids': [], 'product_no_variant_attribute_value_ids': [], 'linked_line_id': False, 'virtual_id': False, 'linked_virtual_id': False, 'selected_combo_items': False, 'combo_item_id': False, 'name': '[E-COM11] Cabinet with Doors', 'product_uom_qty': 1, 'product_uom': 1, 'customer_lead': 0, 'price_unit': 140, 'technical_price_unit': 140, 'tax_id': [], 'product_document_ids': []}]], 'note': False, 'sale_order_option_ids': [], 'quotation_document_ids': [], 'customizable_pdf_form_fields': False, 'user_id': 2, 'team_id': 1, 'require_signature': True, 'require_payment': False, 'prepayment_percent': 1, 'client_order_ref': False, 'tag_ids': [], 'show_update_fpos': False, 'fiscal_position_id': False, 'partner_invoice_id': 27, 'commitment_date': False, 'origin': False, 'campaign_id': False, 'medium_id': False, 'source_id': False}]

        print(f"self.env['sale.order'].create(sale_order_vals) ===> {self.env["sale.order"].create(sale_order_vals)}")


"""
Demo of auto create fields in Model in odoo
"""
class Marks(models.Model):
    _name = "student_marks_stu"
    # this _table is used to give a name to the table on the postgres side regardless of what name is given to the marks model in the _name section
    _table = "my_student_marks_table"
    _description = "This is a marks model for student"

    subject_name = fields.Char(string="Subject Name", required=False)



class sale(models.Model):
    _inherit = "sale.order"

    # @api.model_create_multi
    # def create(self,vals):
    #     print(self,vals)
    #     return super(sale,self).create(vals)

    def write(self, vals):
        print(self,vals)
        return super(sale,self).write(vals)

class saleline(models.Model):
    _inherit = "sale.order.line"

    # @api.model_create_multi
    # def create(self,vals):
    #     print(self,vals)
    #     return super(saleline,self).create(vals)

    def write(self,vals):
        print(self,vals)
        return super(saleline,self).write(vals)


    






















        






