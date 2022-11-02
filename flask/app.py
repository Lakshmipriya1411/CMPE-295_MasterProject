from flask import Flask, request, render_template, jsonify
from surprise import dump 
from pymongo import MongoClient
from bson import json_util
import json
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# MONGODB Info
mongo_uri = "mongodb+srv://cmpe295b:cmpe295bfinalproject@cmpe295bmasterproject.at3cjun.mongodb.net/test"
client = MongoClient(mongo_uri)
db = client.CMPE295BMasterProject
recipe_dataset = db.recipe_dataset

# Local dataset
df = pd.read_csv('../data/recipe_dataset.csv', header = 0)
df_search = df.copy()
df_search = df_search.drop_duplicates(subset="recipe_id")
tfidf_title_vectorizer = TfidfVectorizer()
tfidf_title_features = tfidf_title_vectorizer.fit_transform(df_search['ingredients'])

# Load both models (tfidf not used as of now)
tfidf_vectorizer = pickle.load(open('../models/tfidf_vectorizer.pkl', 'rb'))
tfidf_feature = pickle.load(open('../models/tfidf_feature.pkl', "rb"))
collaborative_filtering_model = dump.load('../models/model.pkl')  

@app.route("/")
def hello_world():
    """
        Simple landing page API
    """
    all_recipe = recipe_dataset.find().limit(10)
    return render_template('index.html', recipes=all_recipe)

@app.route("/vegetarian", methods=["GET"])
def vegan():
    """
        GET api for finding vegetarian recipes
        Returns:
            list of vegetarian recipes
    """
    #all_vegan_recipes = list(recipe_dataset.aggregate( [ { '$match': {'recipe_tags': {'$regex': 'vegan'} } } ]))
    # vegan_df = pd.DataFrame(all_vegan_recipes)
    # local_vegan_df = df[df['recipe_tags'].str.contains('vegan')]

    column_output = ['recipe_id','title','ingredients','recipe_tags','date','directions','description','nutrition','minutes']
    #vegan_recipes = vegan_df.groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
    vegan_recipes = df[df['recipe_tags'].str.contains('vegetarian')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)

    return jsonify(vegan_recipes.to_dict('records'))

@app.route("/nonvegetarian", methods=["GET"])
def non_vegan():
    """
        GET api for finding nonvegetarian recipes
        Returns:
            list of nonvegetarian recipes
    """
    #all_nonvegan_recipes = list(recipe_dataset.aggregate( [ { '$match': {'recipe_tags': {'$regex': 'nonvegan'} } } ]))
    
    column_output = ['recipe_id','title','ingredients','recipe_tags']
    nonvegan_recipes = df[~df['recipe_tags'].str.contains('vegetarian')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)

    return jsonify(nonvegan_recipes.to_dict('records'))

@app.route("/search", methods=["GET"])
def search():
    """
        GET api for searching for recipes. Runs both models (tfidf first then collaborative filtering)
        Returns:
            list of recipes
    """
    ingredients = request.form.get('ingredients')
    user_id = request.form.get('user_id')

    indices = run_tfidf(ingredients, 20)
    str_indices = [str(x) for x in indices]
    recipes = list(recipe_dataset.find( { "" : { "$in" : str_indices } } ) )

    rating_df = pd.DataFrame(recipes)
    rating_df['estimate_rating'] = rating_df['recipe_id'].apply(lambda x: collaborative_filtering_model[1].predict(user_id, x).est)
    rating_df = rating_df.drop_duplicates(subset="recipe_id")
    rating_df = rating_df.sort_values('estimate_rating', ascending=False)

    return parse_json(rating_df.to_dict('records'))

def run_tfidf(input_ner, num_results):
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

def parse_json(data):
    """
        Serializes MongoDB objects with ObjectId. Can't serialize normally if it has it.
        Returns:
            json return object
    """
    return json.loads(json_util.dumps(data))

if __name__ == "__main__":
    app.run()
