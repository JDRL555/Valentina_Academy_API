from mongoengine import Document, StringField, IntField, DateField, BooleanField, ReferenceField, ListField

import datetime

# Create your models here.
class Answers(Document):
  answer = StringField(required=True, max_length=500)
  is_correct = BooleanField(default=False)

class Questions(Document):
  question = StringField(max_length=300, required=True)
  answers_id = ListField(ReferenceField(Answers, required=True, dbref=True, multiple=True))

class Surveys(Document):
  title = StringField(required=True, max_length=50)
  description = StringField(max_length=100)
  course_id = IntField(required=True)
  question_id =  ListField(ReferenceField(Questions, required=True, dbref=True, multiple=True))
  created_at = DateField(default=datetime.datetime.now())
