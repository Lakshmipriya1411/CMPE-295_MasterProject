from api.database.db import db
from flask import Flask, request, render_template
from surprise import dump 
from pymongo import MongoClient
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import numpy as np
import pandas as pd
import pickle
import os
from surprise import Reader, Dataset, SVD, dump, accuracy
from surprise.model_selection import train_test_split, KFold
import random

df = pd.read_csv('~/Downloads/recipe_dataset_new.csv',header=0)
#print(df.tail(3))

df_search = df.copy()
df_search = df_search.drop_duplicates(subset="recipe_id")
tfidf_title_vectorizer = TfidfVectorizer()
tfidf_title_features = tfidf_title_vectorizer.fit_transform(df_search['ingredients'])

# Load both models (tfidf not used as of now)
tfidf_vectorizer = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_vectorizer.pkl"), 'rb'))
tfidf_feature = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_feature.pkl"), "rb"))

class Service:
    def __init__(self,collection) -> None:
        self.collaborative_filtering_model = dump.load(os.path.expanduser('~/Downloads/new_model.pkl'))[1]
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
    def get_list_string(self,values):
        ings = '['
        for indx,i in enumerate(values):
            ings+="'"+str(i)+"'"
            
            if(indx!=len(values)-1):
                ings+=','
        
        ings +=']'
        return ings

    def insert_recipe(self,object):
        user = db.user.find_one({'access_token':object['user_token']})
        recipe = db.recipe_dataset.find_one({'title':object['title']})
        unnamed_id = int(df.tail(1)['Unnamed: 0']) +1
        rated_recipe = db.recipe_dataset.find_one({'title':object['title'],'user_id':user['user_id']})
        recipe_tags = self.get_list_string(object['recipe_tags'])
        recipe_obj = {
            "":str(unnamed_id),
            "title": recipe['title'],
            "minutes": recipe['minutes'],
            "contributor_id": recipe['contributor_id'],
            "recipe_submitted_date": recipe['recipe_submitted_date'],
            "recipe_tags": recipe['recipe_tags'],
            "nutrition": recipe['nutrition'],
            "n_directions": recipe['n_directions'],
            "directions":recipe['directions'],
            "description": recipe['description'],
            "ingredients": recipe['ingredients'],
            "n_ingredients": recipe['n_ingredients'],
            "user_id": user['user_id'],
            "recipe_id": recipe['recipe_id'],
            "date": recipe['date'],
            "user_rating": str(object['user_rating']),
            "user_review": 'Good',
            "image":recipe['image'] if 'image' in recipe else ''
            }
        if not rated_recipe:
            res = db.recipe_dataset.insert_one(recipe_obj)
        else:
            myquery = { "title": object['title'],'user_id':user['user_id']}  
            newvalues = { "$set": { "user_rating": str(object['user_rating']) } }
            res = self.update(myquery,newvalues)
      

        return "Successfully updated the record"

    def find_ingreds(self,collectioname):  # find all
        #print("am here")
        if(collectioname == 'ingredient_datatset'):
            dbi = db.ingredient_datatset
            return (list(dbi.find()))
        elif collectioname == 'ingredient_frequency_map':
            dbi = db.ingredient_frequency_map
            return list(dbi.find())
       
  
    def find(self,collectionname,field,value):
        dbi = db.recipe_dataset
        return list(dbi.find({field:str(value)}).limit(50))
      
    def find_matching(self,collectioname,query):
        return list(db.recipe_dataset.find(query).sort("user_rating", -1).limit(50))


    def find_by_aggregation(self,collection):
      
        res = list(db.recipe_dataset.aggregate([
            {"$match": { "user_rating":"5" } },
            {"$group" : {"_id":"$title", "count":{"$sum":1}}},
            {"$sort": {"count":-1}} ,
            {"$limit":50}
            ]))
   
        return res

    def find_by_reviews(self,collection):
        res = list(db.recipe_dataset.aggregate([
            {"$group" : {"_id":"$title", "count":{"$sum":1}}},
            {"$sort": {"count":-1}} ,
            {"$limit":50}
            ]))
 
 
        return res
  
    def find_auth_one(self,field,value):
        return self.db.find_one({ field: value })

    def find_one_email(self,field,value):
        #print("isuue here")
        return self.db.find_one({ field: value })
#             return jsonify({ "error": "Email address already in use" }), 400
    def find_one(self,collection,field,value):
        return db.recipe_dataset.find_one({ field: value })

    def find_by_id(self, id):
        return self.db.find_by_id(id)

    def update_user(self,query,newValues):
        return self.db.update_one(query,newValues)

    def update(self,query,newvalues):
        return db.recipe_dataset.update_one(query, newvalues)
        return self.db.update(id, object,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
    
    def find_matching_cuisine(self,collection,cuisine):
        print(cuisine)
        lst_res = list( db.recipe_dataset.find({"recipe_tags":{"$regex":cuisine}}).limit(150))
        print("resss")
        #print(lst_res)
        return lst_res

    def find_matching_vegan(Self,colelction):
        #print(df.tail(2))
        column_output = ['recipe_id','title','ingredients','recipe_tags']
        vegan_recipes = df[df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
        #print(vegan_recipes)
        return vegan_recipes.to_dict('records')

    def find_matching_non_vegan(Self,colelction):
        #print(df.tail(2))
        column_output = ['recipe_id','title','ingredients','recipe_tags']
        nonvegan_recipes = df[~df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
        return nonvegan_recipes.to_dict('records')

    def train(self,df):
        def split_train_test(data, svd):
            trainset, testset = train_test_split(data, test_size=0.25)
            #trainset = data.build_full_trainset()
            svd.fit(trainset)
        #df_res = pd.DataFrame(df)

        reader = Reader(rating_scale=(1, 5))
        # Train the dataset
        #reader = Reader()
        svd = SVD()
        data = Dataset.load_from_df(df[['user_id', 'recipe_id', 'user_rating']], reader)
        split_train_test(data, svd)
        
        self.collaborative_filtering_model = svd
   
    def tfidf_model_cold_start(self,input_ner, num_results,cold_start_df):
        tfidf_title_vectorizer_cold_start = TfidfVectorizer()
        tfidf_title_features_cold_start = tfidf_title_vectorizer_cold_start.fit_transform(cold_start_df['ingredients'])
        tfidf_title_features_cold_start[0].todense().shape
        
        input_vector = tfidf_title_vectorizer_cold_start.transform(pd.Series(input_ner))
        pairwise_dist = pairwise_distances(tfidf_title_features_cold_start, input_vector)
        indices = np.argsort(pairwise_dist.flatten())[0:num_results]
        pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
        df_indices = list(cold_start_df.index[indices])
        return df_indices
    def run_tfidf(self,input_ner, num_results):
        """
            Runs cosine similarity, comparing user input of words to dataframe vector.
            Returns:
                dataframe indexes of recipes with closest pairwise distances
        """
        input_vector = tfidf_title_vectorizer.transform(pd.Series(input_ner))
        pairwise_dist = pairwise_distances(tfidf_title_features, input_vector)
        indices = np.argsort(pairwise_dist.flatten())[0:num_results]
        
        #pdists will store the 9 smallest distances
        pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
        
        #data frame indices of the 9 smallest distace's
        df_indices = list(df_search.index[indices])

        return df_indices  

    def search(self,ingredients,user_id):
    #     """
    #         GET api for searching for recipes. Runs both models (tfidf first then collaborative filtering)
    #         Returns:
    #             list of recipes
    #     """
        #indices = self.run_tfidf("['brown sugar', ' milk', ' vanilla', ' nuts', ' butter', ' bite size shredded rice biscuits']", 20)
        ings = '['
        for indx,i in enumerate(ingredients):
            ings+="'"+str(i)+"'"
            
            if(indx!=len(ingredients)-1):
                ings+=','
        
        ings +=']'
        #print("user_id"+user_id)
        indices = self.run_tfidf(ings, 100)
        #print(indices)
        rating_df = df_search.copy()
        rating_df = rating_df[rating_df.index.isin(indices)]
        rating_df.reset_index()
        #prepare input for Collaborative Filtering
        #Step 1. Read ratings from Mongo DB
        dfre = list(db.recipe_dataset.find({'title': { "$in": list(rating_df['title'])} } ))
        dfre_df = pd.DataFrame(dfre)
        #print(dfre_df)
        dfre_df['recipe_id'] = dfre_df['recipe_id'].fillna("0")
        dfre_df['user_id'] = dfre_df['user_id'].fillna("0")
        dfre_df['user_rating'] = dfre_df['user_rating'].fillna("0")
        dfre_con = dfre_df.astype({'recipe_id': 'int64','user_id':'int64','user_rating':'int64'})
        df1 = dfre_con.filter(items=['recipe_id','user_id', 'user_rating'])
        #print(df1)
        #Step 2. Add ratings if the pased in user rated any of these pairwise similarity result recipes
        for ind in rating_df.index:
            title = rating_df['title'][ind]
            
            if not df.loc[(df['title']==title) & (df['user_id'] == int(user_id))].empty:
                dg = df.loc[(df['title']==title) & (df['user_id'] == int(user_id))]
                df1.loc[len(df1.index)] = [int(dg['recipe_id']), int(user_id), int(dg['user_rating'])] 
        #print(df1)

        # Step 3. Find matching ingredients in u(ser rating and get those top 5 records
        #cold_start_df = df.query('user_id=='+str(user_id)+"'")
        cold_start_df=df.query("user_id == "+user_id)
        indi = self.tfidf_model_cold_start(ings, 100,cold_start_df)
        #print("ind")
        #print(indi)
        rating_df_cs = df.copy()
        rating_df_cs = rating_df_cs[rating_df_cs.index.isin(indi)]
        rating_df_cs.reset_index()
        #print(rating_df_cs)
        dfre_ur = db.recipe_dataset.find({ 'title': { '$in': list(rating_df['title']) } ,'user_id':str(user_id)} )
        #print("DF")
        dfre_df = pd.DataFrame(dfre_ur)

        if not dfre_df.empty: 
            dfre_con = dfre_df.astype({'recipe_id': 'int64','user_id':'int64','user_rating':'int64'})
            df1_m = dfre_con.filter(items=['recipe_id','user_id', 'user_rating'])
            df1= df1.append(df1_m, ignore_index=True)
     
        self.train(df1)
        rating_df['estimate_rating'] = rating_df['recipe_id'].apply(lambda x: self.collaborative_filtering_model.predict(user_id, x).est)

        rating_df = rating_df.drop_duplicates(subset="recipe_id")
        rating_df = rating_df.sort_values('estimate_rating', ascending=False)
        rating_df = rating_df[rating_df['estimate_rating'] > 3] 
 
        rating_df = rating_df.head(20)
        return rating_df.to_dict('records')


     