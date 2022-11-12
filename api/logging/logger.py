import logging
import flask
from flask_restx import Api, Resource

app = flask.Flask(__name__)

api = Api(app)

# configure root logger
logging.basicConfig(level=logging.INFO)
# each of these loggers uses configuration from app.logger
signUp = api.namespace('api/auth/signup', description='SignUp Log')
signIn = api.namespace('api/auth/signin', description='SignIn Log')
signOut = api.namespace('api/auth/signout',description='SignOut Log')

ingreds = api.namespace('api/ingredients', description='Ingredients Log')
ingredsFreq = api.namespace('api/ingredients/frequency', description='Ingredients Frequency Log')

logGetCusines = api.namespace('api/recipes/cuisine',description='Cuisine Log')
logGetRecipeByID = api.namespace('api/recipes/cuisine',description='Cuisine Log')
logGetSelectedCusines = api.namespace('api/recipes/cuisine/type',description='Cuisine Log')

logGetDietRecipes = api.namespace('api/recipes/diet', description='Diet Recipes Log')
logGetSelectedDietRecipes = api.namespace('api/recipes/diet/type', description='Selected Diet Log')

logGetPopularRecipes = api.namespace('api/recipes/popular', description='Popular Recipes Log')
logGetPopularRatedRecipes = api.namespace('api/recipes/popular/rating', description='Popular Rated Log')
logGetPopularReviewRecipes = api.namespace('api/recipes/popular/review', description='Popular Review Log')

logGetCookingRecipes = api.namespace('api/recipes/cookingtime', description='Cooking Time Recipes Log')
logGetSelectedCookingRecipes = api.namespace('api/recipes/cookingtime/time', description='Selected Cooking Time Log')

logGetIngredRecipes = api.namespace('api/recipes/ingredient', description='Recipes By Ingred Log')
logGetSelectedIngredRecipes = api.namespace('api/recipes/ingredients/type', description='Selected Ingred Recipe Log')

logUpdateRating = api.namespace('api/recipes/rating', description='Update Rating Log')
logUpdateReview = api.namespace('api/recipes/review', description='Update Review Log')

logSearchRecipe = api.namespace('api/recipe',description="Search Recipe")

fh = logging.FileHandler("api/logging/logs/logInfo.log")
fh.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
signUp.logger.addHandler(fh)
signIn.logger.addHandler(fh)
signOut.logger.addHandler(fh)

ingreds.logger.addHandler(fh)
ingredsFreq.logger.addHandler(fh)

logGetCusines.logger.addHandler(fh)
logGetRecipeByID.logger.addHandler(fh)
logGetSelectedCusines.logger.addHandler(fh)

logGetDietRecipes.logger.addHandler(fh)
logGetSelectedDietRecipes.logger.addHandler(fh)

logGetPopularRecipes.logger.addHandler(fh)
logGetPopularRatedRecipes.logger.addHandler(fh)
logGetPopularReviewRecipes.logger.addHandler(fh)

logGetCookingRecipes.logger.addHandler(fh)
logGetSelectedCookingRecipes.logger.addHandler(fh)

logGetIngredRecipes.logger.addHandler(fh)
logGetSelectedIngredRecipes.logger.addHandler(fh)
#ns2 = api.namespace('api/v2', description='test')
#signIn.logger.setLevel(logging.DEBUG)