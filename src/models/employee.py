import uuid
from datetime import datetime

from src.common.database import Database
from bson.objectid import ObjectId


class Employee(object):

    def __init__(self, name, district, block, panchayat, designation, center_name, DOB=None, last_updated=None,
                 joining_date=None, retirement_date=None, qualification=None, contact_number=None,
                 _id=None, joining_date_current_post=None, nhis_id=None, gpf=None, gender=None):
        self.name = name
        self.district = district
        self.block = block
        self.panchayat = panchayat
        self.designation = designation
        self.center_name = center_name
        self.qualification = qualification
        self.DOB = DOB
        self.joining_date_current_post = joining_date_current_post
        self.nhis_id = nhis_id
        self.gpf = gpf
        self.gender = gender
        self.joining_date = joining_date
        self.retirement_date = retirement_date
        self.contact_number = contact_number
        self._id = uuid.uuid4().hex if _id is None else _id
        if retirement_date:
            self.dorV2 = (datetime.combine(datetime.strptime(retirement_date, '%Y-%m-%d').date(),
                                           datetime.now().time()))
        else:
            self.dorV2 = retirement_date

        if retirement_date:
            self.dorV2 = (datetime.combine(datetime.strptime(retirement_date, '%Y-%m-%d').date(),
                                           datetime.now().time()))
        else:
            self.dorV2 = retirement_date

        if DOB:
            self.dobV2 = (datetime.combine(datetime.strptime(DOB, '%Y-%m-%d').date(),
                                           datetime.now().time()))
        else:
            self.dobV2 = DOB

        if joining_date:
            self.dojV2 = (datetime.combine(datetime.strptime(joining_date, '%Y-%m-%d').date(),
                                           datetime.now().time()))
        else:
            self.dojV2 = joining_date

        if joining_date_current_post:
            self.joining_date_current_postV2 = (datetime.combine(datetime.strptime(joining_date_current_post,
                                                                                   '%Y-%m-%d').date(),
                                                                 datetime.now().time()))
        else:
            self.joining_date_current_postV2 = joining_date_current_post

    def save_to_mongo(self):
        Database.insert(collection='employees', data=self.json())

    @classmethod
    def deletefrom_mongo(cls, _id):
        if Database.is_valid(_id):
            Database.delete_from_mongo(collection='employees', query={'_id': ObjectId(_id)})
        else:
            Database.delete_from_mongo(collection='employees', query={'_id': _id})

    @classmethod
    def update_employee(cls, name, emp_id, district, block, panchayat, designation, center_name, dob, doj, dor,
                        joining_date_current_post, nhis_id, gender, gpf, qualification):

        if dor:
            dorV2 = (datetime.combine(datetime.strptime(dor, '%Y-%m-%d').date(),
                                      datetime.now().time()))
        else:
            dorV2 = dor

        if dob:
            dobV2 = (datetime.combine(datetime.strptime(dob, '%Y-%m-%d').date(),
                                      datetime.now().time()))
        else:
            dobV2 = dob

        if doj:
            dojV2 = (datetime.combine(datetime.strptime(doj, '%Y-%m-%d').date(),
                                      datetime.now().time()))
        else:
            dojV2 = doj

        if joining_date_current_post:
            joining_date_current_postV2 = (datetime.combine(datetime.strptime(joining_date_current_post,
                                                                              '%Y-%m-%d').date(),
                                                            datetime.now().time()))
        else:
            joining_date_current_postV2 = joining_date_current_post

        if Database.is_valid(emp_id):
            Database.update_employee(collection='employees', query={'_id': ObjectId(emp_id)}, emp_name=name,
                                     district=district, block=block, panchayat=panchayat, designation=designation,
                                     center_name=center_name, dob=dob, doj=doj, dor=dor, gpf=gpf,
                                     joining_date_current_post=joining_date_current_post, nhis_id=nhis_id,
                                     gender=gender, joining_date_current_postV2=joining_date_current_postV2,
                                     dobV2=dobV2, dojV2=dojV2, dorV2=dorV2, qualification=qualification)

        else:
            Database.update_employee(collection='employees', query={'_id': emp_id}, emp_name=name, district=district,
                                     block=block, panchayat=panchayat, designation=designation, center_name=center_name,
                                     dob=dob, doj=doj, dor=dor, joining_date_current_post=joining_date_current_post,
                                     nhis_id=nhis_id, gender=gender, gpf=gpf, dobV2=dobV2, dojV2=dojV2,
                                     joining_date_current_postV2=joining_date_current_postV2, dorV2=dorV2,
                                     qualification=qualification)

    def json(self):
        return {
            'Employee Name': self.name,
            'District': self.district,
            'Block': self.block,
            'Name of Village Panchayat': self.panchayat,
            'Designation': self.designation,
            'Name of the Center': self.center_name,
            'Educational Qualification': self.qualification,
            'Contact Number': self.contact_number,
            'Date of Birth': self.DOB,
            'Date of Joining': self.joining_date,
            'Date of Retirement': self.retirement_date,
            'joining_date_current_post': self.joining_date_current_post,
            'Date of BirthV2': self.dobV2,
            'Date of JoiningV2': self.dojV2,
            'Date of RetirementV2': self.dorV2,
            'joining_date_current_postV2': self.joining_date_current_postV2,
            'nhis_id': self.nhis_id,
            'gpf': self.gpf,
            'gender': self.gender,
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
