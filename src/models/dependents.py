from src.common.database import Database

class Dependents(object):

    def __init__(self, beneficiary_id, mother, father, parents_residence, spouse=None, parents_highest_qualification=None,
                 father_occupation=None, mother_occupation=None, number_employed_siblings=None, number_married_siblings=None,
                 siblings_residence=None, no_of_brothers=None, no_of_sisters=None, _id=None):
        self.beneficiary_id = beneficiary_id
        self.mother = mother
        self.father = father
        self.spouse = spouse
        self.no_of_brothers = no_of_brothers
        self.no_of_sisters = no_of_sisters
        self.parents_residence = parents_residence
        self.parents_highest_qualification = parents_highest_qualification
        self.father_occupation = father_occupation
        self.mother_occupation = mother_occupation
        self.number_employed_siblings = number_employed_siblings
        self.number_married_siblings = number_married_siblings
        self.siblings_residence = siblings_residence
        self._id = _id

    def save_to_mongo(self):
        Database.insert(collection='dependents', data=self.json())

    @classmethod
    def from_mongo(cls, beneficiary_id):
        dependents = Database.find_one(collection='dependents', query={'beneficiary_id': beneficiary_id})
        if dependents is not None:
            return [cls(**dep) for dep in dependents]

    def json(self):
        return {
            'beneficiary_id': self.beneficiary_id,
            'mother': self.mother,
            'father': self.father,
            'no_of_brothers': self.no_of_brothers,
            'no_of_sisters': self.no_of_sisters,
            'parents_residence': self.parents_residence,
            'parents_highest_qualification': self.parents_highest_qualification,
            'father_occupation': self.father_occupation,
            'mother_occupation': self.mother_occupation,
            'number_employed_siblings': self.number_employed_siblings,
            'number_married_siblings': self.number_married_siblings,
            'siblings_residence': self.siblings_residence,
            '_id': self._id
        }

