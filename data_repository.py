# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 00:24:25 2022

@author: ddibalaba
"""

from pymongo import MongoClient
from bson import json_util
import pprint
import json
import ast





MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

EpicA={
      "Name":"EpicA",
      "Tasks":["TaskA1", "TaskA2"],
      "Bugs":[],
      "Epics":["EpicB"],
      "status":""
      
      } 

EpicB={
       "Name":"EpicB",
      "Tasks": ["TaskB1", "TaskB2"],
      "Bugs": ["BugB1"],
      "Epics": [""],
      "status":""
      }

EpicC={
       "Name":"EpicC",
       "Tasks": [],
       "Bugs": [],
       "Epics": [],
       "status":""
       }

EpicD={
       
       "Tasks": [],
       "Bugs": [],
       "Epics": ["EpicC"],
       "Name":"EpicD",
       "status":""
       
       }

EpicE={
       "Tasks": [],
       "Bugs": ["BugE1"],
       "Epics": [],
       "Name":"EpicE",
       "status":""
       
       }

##coonect to mongodb
 
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
work= connection.work
connection.drop_database(work)
work.collection.drop()
backlog=work.backlog
backlog.insert_many([EpicA,EpicB,EpicC,EpicD,EpicE])

def db_connector():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    work= connection.work
    connection.drop_database(work)
    work.collection.drop()
    backlog=work.backlog
    backlog.insert_many([EpicA,EpicB,EpicC,EpicD,EpicE])






def get_all():
  list=[]
  for doc in backlog.find():
    list.append(doc)
    
  return json.loads(json_util.dumps(list))

###FilterWorkInprogress

def filterWIP():
    
   epicInProgress=list([obj for obj in backlog.find() if(obj['Tasks']  )])


   for obj in backlog.find():
      for ob in obj['Epics'] :
          if(ob in epicInProgress):
              epicInProgress.append(obj)
              
   for obj in epicInProgress:
       obj['status'] = "work in progress"
       db_connector()
              
              
   return epicInProgress


### blocked epics

def filter_blocked():
    
    blocked_epics=list([obj for obj in backlog.find() if(obj['Bugs'])])
    #print(blocked_epics)
    
    for obj in backlog.find():
       for ob in obj['Epics'] :
           if(ob in blocked_epics):
               blocked_epics.append(obj)
               
    for obj in blocked_epics:
        obj['status'] = "blocked"
        db_connector()
    
    return blocked_epics
    
    
### filter all the bugs related to an epic
    
def filter_bugs_related_to_epic(epic):
   
    ep= backlog.find_one({ "Name" : epic})
    
    # print("ep",ep)
    list_of_related_bugs= list(ep['Bugs'])
    
    
    for obj in ep['Epics']:
            
                for ob in backlog.find():
                    if(ob['Name'] == obj):
                
                      list_of_related_bugs.append(ob['Bugs'])
               
    return list_of_related_bugs


### update your collection 

def update_one_item(condition,new_value):
    
   print('type of new value',type(new_value))
   work.backlog.update_one(ast.literal_eval(condition),{"$set": ast.literal_eval(new_value)})
   for item in backlog.find():
     print(item)
     
     
def update_many_item(condition,new_value):
   work.backlog.update_many(condition,{"$set": new_value})
   
   for item in backlog.find():
     print(item)  
    
    


       
       
    


