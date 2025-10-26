


from tortoise.models import Model
from tortoise import fields


class TimeTable(Model):
    id = fields.IntField(pk=True)
    subject = fields.ForeignKeyField('models.Subject', related_name='timetables')
    lecturer = fields.ForeignKeyField('models.Lecturer', related_name='timetables')
    classroom = fields.ForeignKeyField('models.Classroom', related_name='timetables')
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()