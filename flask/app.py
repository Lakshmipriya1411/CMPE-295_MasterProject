from flask import Flask, request, render_template
from surprise import dump 
from pymongo import MongoClient
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

@app.route("/vegan", methods=["GET"])
def vegan():
    """
        GET api for finding vegan recipes
        Returns:
            list of vegan recipes
    """
    all_vegan_recipes = list(recipe_dataset.aggregate( [ { '$match': {'recipe_tags': {'$regex': 'vegan'} } } ]))
    # vegan_df = pd.DataFrame(all_vegan_recipes)
    # local_vegan_df = df[df['recipe_tags'].str.contains('vegan')]

    column_output = ['recipe_id','title','ingredients','recipe_tags']
    #vegan_recipes = vegan_df.groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
    vegan_recipes = df[df['recipe_tags'].str.contains('vegan')].groupby(column_output)['user_rating'].agg(["count", "mean"]).reset_index().sort_values(by=["mean", "count"], ascending=False).head(20)
    #print(vegan_recipes)

    return render_template('index.html', recipes=vegan_recipes.to_dict('records'))

@app.route("/search", methods=["GET"])
def search():
    """
        GET api for searching for recipes. Runs both models (tfidf first then collaborative filtering)
        Returns:
            list of recipes
    """
    indices = run_tfidf("['brown sugar', ' milk', ' vanilla', ' nuts', ' butter', ' bite size shredded rice biscuits']", 20)
    str_indices = [str(x) for x in indices]
    recipes = list(recipe_dataset.find( { "" : { "$in" : str_indices } } ) )

    rating_df = pd.DataFrame(recipes)
    #print(rating_df)
    rating_df['estimate_rating'] = rating_df['recipe_id'].apply(lambda x: collaborative_filtering_model[1].predict(4470, x).est)
    rating_df = rating_df.drop_duplicates(subset="recipe_id")
    rating_df = rating_df.sort_values('estimate_rating', ascending=False)

    return render_template('index.html', recipes=rating_df.to_dict('records'))

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

# def run_tfidf(input_ner, num_results):
#     input_tfidf = TfidfVectorizer(vocabulary=tfidf_vectorizer.vocabulary_)
#     input_vector = input_tfidf.fit_transform(pd.Series(input_ner))
#     # print(pd.Series([input_ner]).shape)
#     pairwise_dist = pairwise_distances(tfidf_feature, input_vector)
#     # print(pairwise_dist.shape)
#     indices = np.argsort(pairwise_dist.flatten())[0:num_results]
#     #pdists will store the 9 smallest distances
#     pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
#     # print(indices)
#     #data frame indices of the 9 smallest distace's
#     df_indices = list(df_search.index[indices])
#     return df_indices

if __name__ == "__main__":
    app.run()
