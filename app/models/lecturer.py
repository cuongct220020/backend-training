from tortoise.models import Model
from tortoise import fields


class Lecturer(Model):
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE, primary_key=True)