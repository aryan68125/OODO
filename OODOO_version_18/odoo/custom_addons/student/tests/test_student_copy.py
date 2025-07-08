from odoo.tests.common import TransactionCase
class TestStudentCopy(TransactionCase):
    def setup(self):
        super().setup()
        self.Student = self.env["student"]
        self.school = self.env["school"].create({"name": "Test School", "address": "123 Test St"})
        self.student = self.Student.create({
            "name": "Test Student",
            "age": 20,
            "school_id": self.school.id,
            "hobby_ids": [(0, 0, {"name": "Reading"})]
        })
    def test_copy_student(self):
        # Test the copy method
        copied_student = self.student.copy()
        self.assertNotEqual(copied_student.id, self.student.id, "The copied student should have a different ID.")
        self.assertEqual(copied_student.name, self.student.name, "The name of the copied student should match the original.")
        self.assertEqual(copied_student.age, self.student.age, "The age of the copied student should match the original.")
        self.assertEqual(copied_student.school_id.id, self.student.school_id.id, "The school of the copied student should match the original.")
        self.assertEqual(len(copied_student.hobby_ids), len(self.student.hobby_ids), "The number of hobbies in the copied student should match the original.")
        print("Test passed: Student copy method works as expected.")