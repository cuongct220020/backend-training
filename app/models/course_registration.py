
from tortoise.models import Model
from tortoise import fields


class CourseRegistration(Model):
    id = fields.IntField(pk=True)
    student = fields.ForeignKeyField('models.Student', related_name='registrations')
    course = fields.ForeignKeyField('models.Course', related_name='registrations')