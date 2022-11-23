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



#df = pd.read_csv('../recipe_dataset.csv', header = 0)
#df = pd.read_csv('~/Downloads/recipe_dataset.csv', header = 0)
df = pd.read_csv('~/Downloads/recipe_dataset_new.csv',header=0)
print(df.tail(3))
# data = db.recipe_dataset.find()
# df = pd.DataFrame.from_dict(data)

# coll = db.recipe_dataset
# raw_coll = coll.with_options(codec_options=coll.codec_options.with_options(document_class=RawBSONDocument))
# data = raw_coll.find()
# df = pd.DataFrame.from_dict(data)
df_search = df.copy()
df_search = df_search.drop_duplicates(subset="recipe_id")
tfidf_title_vectorizer = TfidfVectorizer()
tfidf_title_features = tfidf_title_vectorizer.fit_transform(df_search['ingredients'])

# Load both models (tfidf not used as of now)
tfidf_vectorizer = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_vectorizer.pkl"), 'rb'))
tfidf_feature = pickle.load(open(os.path.expanduser("~/Downloads/tfidf_feature.pkl"), "rb"))
#collaborative_filtering_model = dump.load(os.path.expanduser('~/Downloads/model.pkl'))
# tfidf_vectorizer = pickle.load(open('~/tfidf_vectorizer.pkl', 'rb'))
# tfidf_feature = pickle.load(open('~/tfidf_feature.pkl', "rb"))
# collaborative_filtering_model = dump.load('../models/model.pkl')  

class Service:
    def __init__(self,collection) -> None:
        self.collaborative_filtering_model = dump.load(os.path.expanduser('~/Downloads/model.pkl'))[1]
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
            "user_review": ''
            }
        if not rated_recipe:
            res = db.recipe_dataset.insert_one(recipe_obj)
        else:
            myquery = { "title": object['title'],'user_id':user['user_id']}  
            newvalues = { "$set": { "user_rating": object['user_rating'] } }
            res = self.update(myquery,newvalues)
      
        df_new = df.iloc[0].copy(deep=True)

        df_new['title'] = object['title']
        df_new['minutes'] = int(object['mins'])
        df_new['contributor_id'] = int(object['contributor_id'])
        df_new['recipe_submitted_date'] = object['recipe_submitted_date']
        df_new['recipe_tags'] = recipe_tags
        df_new['nutrition'] = object['nutrition']
        df_new['n_directions'] = int(object['n_directions'])
        df_new['directions'] = self.get_list_string(object['directions'])
        df_new['description'] = object['description']
        df_new['ingredients'] = recipe['ingredients']
        df_new['n_ingredients'] = int(object['ingredientsCount'])
        df_new['user_id'] = int(user['user_id']) if 'user_id'in user else ''
        df_new['recipe_id'] = int(recipe['recipe_id'])
        df_new['date']= recipe['date']
        df_new['user_rating'] = int(object['user_rating'])
        df_new['user_review'] = ""
     
        df.loc[len(df.index)] = df_new
        df_search.loc[len(df.index)] = df_new
        df.to_csv('~/Downloads/recipe_dataset_new.csv',index=False)

        return "Successfully updated the record"

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
        
        #print(res[0])
      
        #shuffle(res)
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
        print("isuue here")
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
        return db.recipe_dataset.find({"recipe_tags":{"$regex":cuisine}}).limit(50)

    def find_matching_vegan(Self,colelction):
        print(df.tail(2))
        column_output = ['recipe_id','title','ingredients','recipe_tags']
        vegan_recipes = df[df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
        #print(vegan_recipes)
        return vegan_recipes.to_dict('records')

    def find_matching_non_vegan(Self,colelction):
        print(df.tail(2))
        column_output = ['recipe_id','title','ingredients','recipe_tags']
        nonvegan_recipes = df[~df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
        return nonvegan_recipes.to_dict('records')

    def train(self):
        df3 = pd.read_csv('~/Downloads/recipe_dataset_new.csv', header = 0)
        #print("LAST", df.iloc[-1])
        #print("Size", df.size)
        print(df3.tail(3))

        df4 = df3.filter(items=['user_id', 'recipe_id', 'user_rating'])

        def split_train_test(data, svd):
            trainset, testset = train_test_split(data, test_size=0.25)

            #trainset = data.build_full_trainset()
            svd.fit(trainset)

        # Train the dataset
        reader = Reader()
        svd = SVD()
        data = Dataset.load_from_df(df4[['user_id', 'recipe_id', 'user_rating']], reader)
        split_train_test(data, svd)
        self.collaborative_filtering_model = svd

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
        df3 = pd.read_csv('~/Downloads/recipe_dataset_new.csv', header = 0)
        ings = '['
        for indx,i in enumerate(ingredients):
            ings+="'"+str(i)+"'"
            
            if(indx!=len(ingredients)-1):
                ings+=','
        
        ings +=']'
        print("user_id"+user_id)
        indices = self.run_tfidf(ings, 120)
        #str_indices = [str(x) for x in indices]
        #recipes = list(db.recipe_dataset.find( { "" : { "$in" : str_indices } } ) )
       # print(recipes)
       # rating_df = pd.DataFrame(recipes)
       
        rating_df = df3.copy()
  
        rating_df = rating_df[rating_df.index.isin(indices)]
        rating_df.reset_index()
        rating_df['estimate_rating'] = rating_df['recipe_id'].apply(lambda x: self.collaborative_filtering_model.predict(user_id, x).est)
        #print(rating_df.to_dict('records'))
        rating_df = rating_df.drop_duplicates(subset="recipe_id")
        rating_df = rating_df.sort_values('estimate_rating', ascending=False)
        print(rating_df.to_dict('records'))
        return rating_df.to_dict('records')
         # return render_template('index.html', recipes=rating_df.to_dict('records'))

     