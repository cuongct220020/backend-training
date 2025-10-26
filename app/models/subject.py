

from tortoise.models import Model
from tortoise import fields


class Subject(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    course = fields.ForeignKeyField('models.Course', related_name='subjects')