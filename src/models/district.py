import uuid

from src.common.database import Database

class District(object):

    def __init__(self, block, district, accountHead, MonthYear, amount_sanctioned, amount_spent, _id=None):
        self.block = block
        self.district = district
        self.accountHead = accountHead
        self.MonthYear = MonthYear
        self.amount_sanctioned = amount_sanctioned
        self.amount_spent = amount_spent
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update_district(collection='district_nmp', query=self.json(), sanctioned=self.amount_sanctioned, expenditure=self.amount_spent)

    def json(self):
        return {
            'block': self.block,
            'district': self.district,
            'accountHead': self.accountHead,
            'MonthYear': self.MonthYear
        }

    @classmethod
    def get_by_district(cls, district):
        district = Database.find_one(collection='district_nmp', query={'district': district})
        return cls(**district)

    @classmethod
    def get_by_condition(cls, condition):
        cond = Database.find_one(collection='district_nmp', query={'condition': condition})
        return cls(**cond)


