from flask import Flask, jsonify, request, session, redirect
from numpy import NaN
from api.database import db
from api.service.service import Service
from bson import ObjectId
import ast
from flask import Flask, request, render_template
from random import shuffle


class RecipeModel:
        def __init__(self):
            self.db = db
            self.collection_name = 'recipe_datatset'  # collection name
          
        def get_recipes_by_cuisine_type(self):
            #print("yes here")
            cuisines = ['american', 'canadian', 'european', 'italian', 'mexican', 'thai', 'chinese', 'african', 'indian', 'french', 'greek' ]
            ser = Service(self.collection_name)
            query = {"recipe_tags":{"$exists":cuisines}}
            res =  ser.find_matching(self.collection_name,query)

            lst = []
            for recipe in res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients'] if 'ingredients' in recipe else ''
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst
        
        def get_recipes_by_selected_cuisine_type(self,cuisine):
            #print("yes here")
            #cuisines = ['american', 'canadian', 'european', 'italian', 'mexican', 'thai', 'chinese', 'african', 'indian', 'french', 'greek' ]
            ser = Service(self.collection_name)
            #query = {"recipe_tags":{"$exists":cuisine}}
            #query = { tags: "red" } )

            res =  ser.find_matching_cuisine(self.collection_name,cuisine)
            #print("res")
            #print(list(res))
            #del res['_id']
            result = list(map(dict, set(tuple(sorted(sub.items())) for sub in res)))
            #res = []
            titles =[]
            for tit in result:
                titles.append(tit['title'])
            titleslst = []
            [titleslst.append(x) for x in titles if x not in titleslst]
            #print(titleslst)
            final_res=[]
            for re in res:
                if re['title'] in titleslst:
                    #print(re['title'])
                    titleslst.remove(re['title'])
                    #print(titleslst)
                    final_res.append(re)
            #return result
            #print(res)
            lst = []
            for recipe in final_res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst
           
        def get_selected_recipe_by_id(self,recipe_id):
            ser = Service(self.collection_name)
            #print('find')
            recipe = ''
            if(len(recipe_id) >= 12):
                #print("hello" +recipe_id)
                recipe =  ser.find_one('recipe_dataset','_id',ObjectId(recipe_id))
               
            else:
                #print("hello in else" +recipe_id)
                recipe =  ser.find_one('recipe_dataset','recipe_id',recipe_id)

            #print("recipe_id"+str(recipe_id))
            #print(recipe)
            lstitem = {}
            lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
            lstitem['title'] = recipe['title'] if 'title' in recipe else ''
            lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
            lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
            lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
            lstitem['recipe_tags'] = ast.literal_eval(recipe['recipe_tags']) if 'recipe_tags' in recipe else ''
            lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
            lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
            lstitem['directions'] = ast.literal_eval(recipe['directions']) if 'directions' in recipe else ''
            lstitem['description'] = recipe['description'] if 'description' in recipe else ''
            lstitem['rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
            lstitem['ingredients'] = ast.literal_eval(recipe['ingredients'])
            lstitem['image'] = recipe['image'] if 'image' in recipe else ''
            return lstitem

        def get_recipes_by_diet_type(self):
            diets = ['low-protein', 'low-cholesterol', 'low-fat', 'low-calorie', 'low-carbs', 'low-sodium', 'very-low-carbs', 'high-protein', 'high-calcium','low-saturated-fat']
            ser = Service(self.collection_name)
            query = {"recipe_tags":{"$exists":diets}}
            res =  ser.find_matching(self.collection_name,query)

            lst = []
            for recipe in res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst

        def get_recipes_by_selected_diet_type(self, diet):
            ser = Service(self.collection_name)
            query = {"recipe_tags":{"$exists":diet}}
            res =  ser.find_matching(self.collection_name,query)

            lst = []
            for recipe in res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst

        def get_recipes_by_popularity(self):
            ser = Service(self.collection_name)
            # query = db.teams.aggregate([
  		    #     {$group : {_id:"$position", count:{$sum:1}}},
    		#     {$sort: {count:1}} ,
            #     all:{
			#         $push: “$$ROOT”
			#         }
			#     }
		    # })
            res =  ser.find_by_aggregation(self.collection_name)
            lst = []
            for lstitem in res:
                recipe = self.get_recipes_by_title(lstitem["_id"])
                #print(recipe['id'])
                lstitem['_id'] = str(recipe['id']) if 'id' in recipe else ''
                lstitem['id'] = recipe['recipe_id'] if 'recipe_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['mins'] if 'mins' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['rating'] = recipe["rating"] if 'rating' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                #lst.append(lstitem)
            #print("in modedl res")
            #print(res)
            results = []

            for re in res:
                #print(re)
                if(re['rating'] == "5"):
                    results.append(re)

            shuffle(results)

            return results

        def get_recipes_by_title(self,title):
            #print("title")
            ser = Service(self.collection_name)
            recipe = ser.find_one(self.collection_name,"title",title)
            lst = []
            #print("kjs")
            # print(recipe)
            lstitem = {}
            lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
            lstitem['title'] = recipe['title'] if 'title' in recipe else ''
            lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
            lstitem['recipe_id'] = recipe['recipe_id'] if 'recipe_id' in recipe else ''
            lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
            lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
            lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
            lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
            lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
            lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
            lstitem['description'] = recipe['description'] if 'description' in recipe else ''
            lstitem['ingredients'] = recipe['ingredients']
            lstitem['rating'] = recipe["user_rating"]
            lstitem['image'] = recipe['image'] if 'image' in recipe else ''
            return lstitem
        
        def get_recipes_by_rating(self,rating):
            #print("rating")
            ser = Service(self.collection_name)
            recipes = ser.find(self.collection_name,"user_rating",rating)
            #print("ratingrecipe")
            lst = []
            for recipe in recipes:
                lstitem = {}
                lstitem['_id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst

        def get_recipes_by_review(self):
            ser = Service(self.collection_name)
            res = ser.find_by_reviews(self.collection_name)
            #print("ratingrecipe")
          
            #res =  ser.find_by_aggregation(self.collection_name)
     
            for lstitem in res:
                recipe = self.get_recipes_by_title(lstitem["_id"])
                #print(recipe['id'])
                lstitem['_id'] = str(recipe['id']) if 'id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                #lst.append(lstitem)
            #"in modedl res")
            #print(res)
            return res

        def get_recipes_by_cooking_time(self):
            ser = Service(self.collection_name)
            #cookingtimes = ['low-protein', 'low-cholesterol', 'low-fat', 'low-calorie', 'low-carbs', 'low-sodium', 'very-low-carbs', 'high-protein', 'high-calcium','low-saturated-fat']
            times = ['30-minutes-or-less','15-minutes-or-less','60-minutes-or-less']
            ser = Service(self.collection_name)
            query = {"recipe_tags":{"$exists":times}}
            recipes =  ser.find_matching(self.collection_name,query)
            #recipes = ser.find_by_cookingtime(self.collection_name)
            lst = []
            for recipe in recipes:
                lstitem = {}
                lstitem['_id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lst.append(lstitem)
            
            return lst    

        def get_recipes_by_selected_cooking_time(self,cookingtime):
            ser = Service(self.collection_name)
            query = {"recipe_tags":{"$exists":cookingtime}}
            res =  ser.find_matching(self.collection_name,query)

            lst = []
            for recipe in res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst    

        def get_recipes_by_selected_ingredient(self,ingredient):
            ser = Service(self.collection_name)
            query = {"ingredients":{"$exists":ingredient}}
            res =  ser.find_matching(self.collection_name,query)

            lst = []
            for recipe in res:
                lstitem = {}
                lstitem['id'] = str(recipe['_id']) if '_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['user_rating'] = recipe['user_rating'] if 'user_rating' in recipe else ''
                lstitem['image'] = recipe['image'] if 'image' in recipe else ''
                lst.append(lstitem)
            
            return lst  
        
        def get_recipes_by_selected_ingredients(self,ingredients,token):
            ser = Service(self.collection_name)
            #query = {"ingredients":{"$exists":ingredients}}
            #print("wat")
            u = db.user_dataset.find_one({'access_token':token})
            #print(u)
            res = ser.search(ingredients,u['user_id'])
            #import pdb;pdb.set_trace()
            #import math
            #print("res")
            #res = [0 if math.isnan(x) else x for x in res]
            lst = []
            for recipe in res:
                lstitem = {}
                #print(recipe)
                if 'recipe_id' in recipe and recipe['recipe_id']!='NaN': 
                    lstitem['id'] =  str(recipe['recipe_id']) 
                else :
                    lstitem['id']=''
                if 'title' in recipe and recipe['title']!='NaN': 
                    lstitem['title'] = recipe['title'] 
                else :
                    lstitem['title']=''
                if 'mins' in recipe and recipe['mins']!='NaN': 
                    lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else '' 
                else :
                    lstitem['mins']=''
                if 'contributor_id' in recipe and recipe['contributor_id']!='NaN': 
                     lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                else :
                    lstitem['contributor_id']=''
                if 'recipe_submitted_date' in recipe and recipe['recipe_submitted_date']!='NaN': 
                    lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                else :
                    lstitem['recipe_submitted_date']=''

                if 'recipe_tags' in recipe and recipe['recipe_tags']!='NaN': 
                    lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                else :
                    lstitem['recipe_tags']=''
                if 'nutrition' in recipe and recipe['nutrition']!='NaN': 
                    lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                else :
                    lstitem['nutrition']=''

                if 'n_directions' in recipe and recipe['n_directions']!='NaN': 
                     lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                else :
                    lstitem['n_directions']=''
                if 'directions' in recipe and recipe['title']!='NaN': 
                     lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''     
                else :
                    lstitem['directions']=''
                if 'description' in recipe and recipe['description']!='NaN': 
                     lstitem['description'] =  recipe['description'] if recipe['description']!='NaN' else '' if 'description' in recipe else ''
                else :
                    lstitem['description']=''

                if 'user_rating' in recipe and recipe['user_rating']!='NaN': 
                      lstitem['rating'] = recipe["user_rating"] if 'user_rating' in recipe else ''
                else :
                    lstitem['rating']=''
                if 'review' in recipe and recipe['review']!='NaN': 
                    lstitem['review'] = recipe["user_review"] if 'user_review' in recipe else ''
                else :
                    lstitem['review']=''
                if 'ingredients' in recipe and recipe['ingredients']!='NaN': 
                     lstitem['ingredients'] = recipe['ingredients']
                else :
                    lstitem['ingredients']=''

                if 'image' in recipe and recipe['image']!='NaN': 
                      lstitem['image'] = '' if recipe['image']=='NaN' else recipe['image'] if 'image' in recipe else ''
                else :
                    lstitem['image']=''
                
                #print(lstitem)
                lst.append(lstitem)
            
            #print(lst)
            return lst
        
        def update_rating(self,recipe):
            ser = Service(self.collection_name)
            return ser.insert_recipe(recipe)

        def update_review(self,recipe):
            ser = Service(self.collection_name)
            return ser.insert_recipe(recipe)

        def get_vegan_recipes(self):
            ser = Service(self.collection_name)
            #query = {"recipe_tags":{"$exists":cookingtime}}
            res =  ser.find_matching_vegan(self.collection_name)
            #print(res)
            lst = []
            for recipe in res:
                lstitem = {}
                #print(recipe)
                result  = ser.find_one(self.collection_name,"title",recipe['title'])
                lstitem['id'] = str(recipe['recipe_id']) if 'recipe_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['rating'] = recipe.get("user_rating") if 'user_rating' in recipe else ''
                lstitem['review'] = recipe.get("user_review") if 'user_review' in recipe else ''
                lstitem['image'] = result['image'] if 'image' in result else ''
                #print(lstitem['image'])
                lst.append(lstitem)
            
            return lst    

        def get_non_vegan_recipes(self):
            ser = Service(self.collection_name)
            #query = {"recipe_tags":{"$exists":cookingtime}}
            res =  ser.find_matching_non_vegan(self.collection_name)
            #print(res)
            lst = []
            for recipe in res:
                lstitem = {}
                result  = ser.find_one(self.collection_name,"title",recipe['title'])
                lstitem['id'] = str(recipe['recipe_id']) if 'recipe_id' in recipe else ''
                lstitem['title'] = recipe['title'] if 'title' in recipe else ''
                lstitem['mins'] = recipe['minutes'] if 'minutes' in recipe else ''
                lstitem['contributor_id'] = recipe['contributor_id'] if 'contributor_id' in recipe else ''
                lstitem['recipe_submitted_date'] = recipe['recipe_submitted_date'] if 'recipe_submitted_date' in recipe else ''
                lstitem['recipe_tags'] = recipe['recipe_tags'] if 'recipe_tags' in recipe else ''
                lstitem['nutrition'] = recipe['nutrition'] if 'nutrition' in recipe else ''
                lstitem['n_directions']= recipe['n_directions'] if 'n_directions' in recipe else ''
                lstitem['directions'] = recipe['directions'] if 'directions' in recipe else ''
                lstitem['description'] = recipe['description'] if 'description' in recipe else ''
                lstitem['ingredients'] = recipe['ingredients']
                lstitem['rating'] = recipe.get("user_rating") if 'user_rating' in recipe else ''
                lstitem['review'] = recipe.get("user_review") if 'user_review' in recipe else ''
                lstitem['image'] = result['image'] if 'image' in result else ''               
                lst.append(lstitem)
            
            return lst   

        def re_train_model(self):
            ser = Service(self.collection_name)
            res = ser.train()


       

            

           
      