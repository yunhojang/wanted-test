from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm.queryset import QuerySet
from pymodm.manager import Manager

from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/wanted")


class CompanyInfo(MongoModel):
    company_ko = fields.CharField()
    company_en = fields.CharField()
    company_ja = fields.CharField()
    tag_ko = fields.ListField(fields.CharField(max_length=100))
    tag_en = fields.ListField(fields.CharField(max_length=100))
    tag_ja = fields.ListField(fields.CharField(max_length=100))
