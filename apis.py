# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:38:00 2022

@author: ddibalaba
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import data_repository
import json
import json_util
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

###Endpoint definition

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class ParseBacklog(Resource):
    
    def get(self):
        
        return data_repository.get_all()


class ListAllEpicsInBacklog():
    
    
    def get(self):
        
        return data_repository.get_all()


class ListAllBlockedEpicsFromBugNames(Resource):
    def get(self):
        
        return JSONEncoder().encode(data_repository.filter_blocked())


class ListAllBugsFromEpic(Resource):
    
    def post(self):
        
        parser = reqparse.RequestParser()  
        parser.add_argument('epic', required=True)  
        args = parser.parse_args()
        return data_repository.filter_bugs_related_to_epic(args['epic'])
        

class AddBugOrTaskToEpic(Resource):
    
    def post(self):
        
        parser = reqparse.RequestParser()  
        parser.add_argument('condition', required=True)  
        parser.add_argument('new_value', required=True)
        args = parser.parse_args()
        print(args['condition'],args['new_value'])
        cond= args['condition']
        print('cond',ast.literal_eval(cond))
        new_v= args['new_value']
        
        
        return data_repository.update_one_item(ast.literal_eval(cond),ast.literal_eval(new_v))

class DeleteBugOrTaskToEpic(Resource):
    
    ###UNDER CONSTRUCTION
    pass

class BacklogAsDictionary(Resource):
    
    ###UNDER CONSTRUCTION
    pass


  ###create endpoints
  
api.add_resource(ParseBacklog,'/parseBacklog')
api.add_resource(AddBugOrTaskToEpic,'/AddBugOrTaskToEpic')
api.add_resource(ListAllBugsFromEpic,'/ListAllBugsFromEpic')
api.add_resource(ListAllBlockedEpicsFromBugNames,'/ListAllBlockedEpicsFromBugNames')

if __name__ == '__main__':
     app.run()



