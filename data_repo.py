# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:13:47 2022

@author: ddibalaba
"""

from mongoengine import connect

from mongoengine import Document, ListField, StringField, URLField
from mongoengine.connection import disconnect



connection=connect(db="work_new",alias='test', host="localhost", port=27017)
print(connection)

disconnect(alias='test')





class Epic(Document):
    
    bugs = ListField(required= False, max_length=20)
    epics = ListField(StringField(max_length=20))
    tasks = ListField(required=False)
    
    
EpicA = Epic(
    #name= "EpicA",
    tasks= ["TaskA1", "TaskA2"],
    bugs= [],
    epics= ["EpicB"]
    
    )


EpicA.save()

for doc in Epic.objects:
    print(doc.epics)