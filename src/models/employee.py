import uuid
from src.common.database import Database
from bson.objectid import ObjectId

class Employee(object):

    def __init__(self, name, district, block, panchayat, designation, center_name, DOB,
                 joining_date, retirement_date, qualification, contact_number=None, _id=None):
        self.name = name
        self.district = district
        self.block = block
        self.panchayat = panchayat
        self.designation = designation
        self.center_name = center_name
        self.qualification = qualification
        self.DOB = DOB
        self.joining_date = joining_date
        self.retirement_date = retirement_date
        self.contact_number = contact_number
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='employees', data=self.json())

    @classmethod
    def update_employee(cls, name, emp_id, district, block, panchayat, designation, center_name, dob, doj, dor):
        Database.update_employee(collection='employees', query={'_id': ObjectId(emp_id)}, emp_name=name, district=district,
                                 block=block, panchayat=panchayat, designation=designation, center_name=center_name,
                                 dob=dob, doj=doj, dor=dor)

    def json(self):
        return {
            'Employee Name': self.name,
            'District': self.district,
            'Block': self.block,
            'Name Of Village Panchayat': self.panchayat,
            'Designation': self.designation,
            'Name of the Center': self.center_name,
            'Educational Qualification': self.qualification,
            'Contact Number': self.contact_number,
            'Date Of Birth': self.DOB,
            'Date Of Joining': self.joining_date,
            'Date Of Retirement': self.retirement_date,
            '_id': self._id,
        }

    @classmethod
    def from_mongo(cls, _id):
        Employee = Database.find_one(collection='employees', query={'_id': _id})
        return cls(**Employee)

    @classmethod
    def find_by_block(cls, block):
        employee = Database.find(collection='employees', query={'Block': block})
        return [cls(**emp) for emp in employee]

    @staticmethod
    def from_mongo_blog():
        return [employee for employee in Database.find(collection='employees', query={})]

    @staticmethod
    def from_mongo_employee(block):
        return [beneficiary for beneficiary in Database.find(collection='employees', query={'Block': block})]
