from flask import Flask, jsonify, request, session, redirect
from api.database import db
from api.service.service import Service

class IngredientsModel:
        def __init__(self):
            self.db = db
            self.collection_name = 'ingredient_datatset'  # collection name
          
        def get_ingredients(self):
            ser = Service(self.collection_name)
            #print('find')
            res =  ser.find_ingreds(self.collection_name)
            lst = []
            for i in res:
                lst.append(i['0'])
            #print(lst)
            return lst

        def get_ingredients_frequency_map(self):
            ser = Service('ingredient_frequency_map')
            #print('find')
            res =  ser.find_ingreds('ingredient_frequency_map')
            return res

           
           