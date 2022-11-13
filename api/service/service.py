from api.database.db import db
# from flask import Flask, request, render_template
# from surprise import dump 
# from pymongo import MongoClient
# from sklearn.metrics import pairwise_distances
# from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
# import numpy as np
# import pandas as pd
# import pickle
# import os

#df = pd.read_csv('../recipe_dataset.csv', header = 0)
#df = pd.read_csv('~/Downloads/recipe_dataset.csv', header = 0)
#df = db.recipe_dataset.find()

# df_search = df.copy()
# df_search = df_search.drop_duplicates(subset="recipe_id")
# tfidf_title_vectorizer = TfidfVectorizer()
# tfidf_title_features = tfidf_title_vectorizer.fit_transform(df_search['ingredients'])

# Load both models (tfidf not used as of now)
# tfidf_vectorizer = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_vectorizer.pkl"), 'rb'))
# tfidf_feature = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_feature.pkl"), "rb"))
# collaborative_filtering_model = dump.load(os.path.expanduser('~/Downloads/model.pkl'))
# tfidf_vectorizer = pickle.load(open('~/tfidf_vectorizer.pkl', 'rb'))
# tfidf_feature = pickle.load(open('~/tfidf_feature.pkl', "rb"))
# collaborative_filtering_model = dump.load('../models/model.pkl')  

class Service:
    def __init__(self,collection) -> None:
        self.collection_name = collection
        if(collection == 'user'):
            self.db = db.user
        elif collection == 'ingredients':
            #print("its ingreds")
            self.db = db.ingredient_dataset

    def insert(self,object):
        res = self.db.insert_one(object)
        #print(res.inserted_id)
        #db.user_dataset.insert_one(user)
        return "Inserted Id " + str(res.inserted_id)
    
    def insert_recipe(self,object):
        res = db.recipe_dataset.insert_one(object)
        #print(res.inserted_id)
        #db.user_dataset.insert_one(user)
        return "Inserted Id " + str(res.inserted_id)

    def find_ingreds(self,collectioname):  # find all
        #print("am here")
        if(collectioname == 'ingredient_datatset'):
            dbi = db.ingredient_datatset
            return (list(dbi.find()))
        elif collectioname == 'ingredient_frequency_map':
            dbi = db.ingredient_frequency_map
            return list(dbi.find())
       
            # for doc in dbi.find():
            #     print(doc)
    def find(self,collectionname,field,value):
        dbi = db.recipe_dataset
        return list(dbi.find({field:str(value)}).limit(50))
      
    def find_matching(self,collectioname,query):
        return list(db.recipe_dataset.find(query).sort("user_rating", -1).limit(50))

        # print("res")
        # for i in res:
        #     print("ASfdsfabhi bahi")
        #     print(i)

    def find_by_aggregation(self,collection):
        
        # db.recipe_dataset.aggregate({
  		#             "$group" : {"title":{"$title"}, "review_count":{"$sum":-1},all:{"$push":"$$ROOT"}}
        #             });
       # print("res")
        # res = db.recipe_dataset.aggregate([
        #     { "$group": { "title": "title", "review_count": {"$sum": -1 } },all:{"$push":"$$ROOT"} },
        #     { "$limit": 5},
        #     { "$sort":{"user_rating":-1}}
        #     ] )
        res = list(db.recipe_dataset.aggregate([
            {"$match": { "user_rating":"5" } },
            {"$group" : {"_id":"$title", "count":{"$sum":1}}},
            {"$sort": {"count":-1}} ,
            {"$limit":50}
            ]))
 
       # print(res)
        return res

    def find_by_reviews(self,collection):
        res = list(db.recipe_dataset.aggregate([
            {"$group" : {"_id":"$title", "count":{"$sum":1}}},
            {"$sort": {"count":-1}} ,
            {"$limit":50}
            ]))
 
       # print(res)
        return res
  
    def find_auth_one(self,field,value):
        return self.db.find_one({ field: value })

    def find_one_email(self,field,value):
        return self.db.find_one({ field: value })
#             return jsonify({ "error": "Email address already in use" }), 400
    def find_one(self,collection,field,value):
        return db.recipe_dataset.find_one({ field: value })

    def find_by_id(self, id):
        return self.db.find_by_id(id)

    def update(self,query,newvalues):
        #print("am here too ")
        return db.recipe_dataset.update_one(query, newvalues)
        return self.db.update(id, object,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)

    # def find_matching_vegan(Self,colelction):
    #     print("ia msfndfdj")
    #     column_output = ['recipe_id','title','ingredients','recipe_tags']
    #     vegan_recipes = df[df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False)
    #     return vegan_recipes.to_dict('records')

    # def find_matching_non_vegan(Self,colelction):
    #     column_output = ['recipe_id','title','ingredients','recipe_tags']
    #     nonvegan_recipes = df[~df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
    #     return nonvegan_recipes.to_dict('records')

    # def run_tfidf(self,input_ner, num_results):
    #     """
    #         Runs cosine similarity, comparing user input of words to dataframe vector.
    #         Returns:
    #             dataframe indexes of recipes with closest pairwise distances
    #     """
    #     input_vector = tfidf_title_vectorizer.transform(pd.Series(input_ner))
    #     pairwise_dist = pairwise_distances(tfidf_title_features, input_vector)
    #     indices = np.argsort(pairwise_dist.flatten())[0:num_results]
        
    #     #pdists will store the 9 smallest distances
    #     pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
        
    #     #data frame indices of the 9 smallest distace's
    #     df_indices = list(df_search.index[indices])

    #     return df_indices  

    # def search(self,ingredients):
    # #     """
    # #         GET api for searching for recipes. Runs both models (tfidf first then collaborative filtering)
    # #         Returns:
    # #             list of recipes
    # #     """
    #     #indices = self.run_tfidf("['brown sugar', ' milk', ' vanilla', ' nuts', ' butter', ' bite size shredded rice biscuits']", 20)
    #     ings = '['
    #     for indx,i in enumerate(ingredients):
    #         ings+="'"+str(i)+"'"
            
    #         if(indx!=len(ingredients)-1):
    #             ings+=','
        
    #     ings +=']'
    #     #print("ings"+ings)
    #     #ingres = ings
    #     indices = self.run_tfidf(ings, 20)
    #     str_indices = [str(x) for x in indices]
    #     recipes = list(db.recipe_dataset.find( { "" : { "$in" : str_indices } } ) )

    #     rating_df = pd.DataFrame(recipes)
    #     #print(rating_df)
    #     rating_df['estimate_rating'] = rating_df['recipe_id'].apply(lambda x: collaborative_filtering_model[1].predict(4470, x).est)
    #     rating_df = rating_df.drop_duplicates(subset="recipe_id")
    #     rating_df = rating_df.sort_values('estimate_rating', ascending=False)
    #     print("result of search tfidf")
    #     #print(rating_df.to_dict('records'))
    #     return rating_df.to_dict('records')
         # return render_template('index.html', recipes=rating_df.to_dict('records'))

     