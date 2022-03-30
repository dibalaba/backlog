# -*- coding: utf-8 -*-


from flask import Flask
from flask_mongoengine import MongoEngine
import mongoengine as me
from mongoengine import connect
from mongoengine import Document, ListField, StringField, URLField
from mongoengine.connection import disconnect


disconnect(alias='default')
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "myapp",
}
db = MongoEngine(app)




class Epic(me.Document):
    bugs = me.ListField(required= False, max_length=20)
    epics = me.ListField(me.StringField(max_length=20))
    tasks = me.ListField(required=False)
    
    
EpicA = Epic(
    #name= "EpicA",
    tasks= ["TaskA1", "TaskA2"],
    bugs= [],
    epics= ["EpicB"]
    
    )

EpicA.save()

for doc in Epic.objects:
    print(doc.epics)