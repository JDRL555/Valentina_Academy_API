from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField
import datetime

class Ingredients(Document):
    name = StringField(required=True, max_length=100)

class Recipes(Document):
    name = StringField(required=True, max_length=100)
    description = StringField(max_length=300)
    ingredient = ListField(ReferenceField(Ingredients, dbref=True, multiple=True))
    steps = ListField(StringField(max_length=500))
    created_at = DateTimeField(default=datetime.datetime.now)
