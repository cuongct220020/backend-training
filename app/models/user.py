


from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    user_role = fields.CharField(max_length=50)

    def __str__(self):
        return f"User ID: {self.id}, Name: {self.first_name} {self.last_name}, Email: {self.email}"