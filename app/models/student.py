from tortoise.models import Model
from tortoise import fields


class Student(Model):
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE, primary_key=True)
    age = fields.IntField(null=True)
    gender = fields.CharField(max_length=10, null=True)
    address = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=20, null=True)
    department = fields.CharField(max_length=255, null=True)
    major = fields.CharField(max_length=255, null=True)
    enrollment_year = fields.IntField(null=True)
    class_id = fields.IntField(null=True)


