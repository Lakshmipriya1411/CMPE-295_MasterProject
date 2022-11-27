from flask import request
from api.database.model import recipes
from flask_restful import Resource
from api.logging.logger import logGetCusines, logGetCookingRecipes, logGetRecipeByID, logGetSelectedCusines, logGetSelectedCookingRecipes, logGetCookingRecipes, logGetDietRecipes, logGetIngredRecipes, logGetPopularRatedRecipes, logGetPopularRecipes, logGetPopularReviewRecipes, logGetSelectedDietRecipes, logGetSelectedIngredRecipes
from api.logging.logger import logUpdateRating, logUpdateReview, logSearchRecipe
import json
import ast

recipeModel = recipes.RecipeModel()

class GetRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetCusines.logger.info("------------------Enter get Recipes By All Cusine Types---------------")
            recipeslst = recipeModel.get_recipes_by_cuisine_type()
            logGetCusines.logger.info("Got Recipes By All Cusine Types successfully")
            logGetCusines.logger.info("------------------End of Get Recipes By All Cusine Types---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetCusines.logger.error("Error processing the request")
            logGetCusines.logger.error(ex)
            raise ex

class GetSelectedRecipeApi(Resource):
    @cross_origin()
    def post(self):
        try:
            logGetRecipeByID.logger.info("------------------Enter get Recipes By Selected RecipeID--------------")
            rcp = request.get_json()
            recipe_id = rcp.get('recipe_id')
            recipe = recipeModel.get_selected_recipe_by_id(recipe_id)
            logGetRecipeByID.logger.info("Get Selected Recipe By Id success")
            logGetRecipeByID.logger.info("------------------End of Get Reipes By Selected RecipeID---------------")
            return recipe, 200

        except Exception as ex:
            logGetRecipeByID.logger.error("Error processing the request")
            # raise ex
            logGetRecipeByID.logger.error(ex)
            return {'error': 'Error processing the request'}, 400


class GetCuisineRecipesApi(Resource):
    @cross_origin()
    def post(self):
        try:
            logGetSelectedCusines.logger.info("------------------Enter get REcipes By Cusine Type---------------")
            rcp = request.get_json()
            csn = rcp.get('cuisine')
            print("cuisine set"+csn)
            recipeslst = recipeModel.get_recipes_by_selected_cuisine_type(csn)
            
            logGetSelectedCusines.logger.info("Get Selected Recipe By Cusine success")
            logGetSelectedCusines.logger.info("------------------End of Get REcipes By Cusine Type---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetSelectedCusines.logger.error("Error processing the request")
            raise ex
            logGetSelectedCusines.logger.error(ex)
            return {'error': 'Error processing the request'}, 400


class GetSelectedDietRecipesApi(Resource):
    @cross_origin()
    def post(self):
        try:
            logGetSelectedDietRecipes.logger.info("------------------Enter get Recipes By Selected Diet Type---------------")
            rcp = request.get_json()
            csn = rcp.get('diet')
            recipeslst = recipeModel.get_recipes_by_selected_diet_type(csn)
            logGetSelectedDietRecipes.logger.info("Get Selected Recipe By Diet success")
            logGetSelectedDietRecipes.logger.info("------------------End of Get REcipes By Selected Diet Type---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetSelectedDietRecipes.logger.error("Error processing the request")
            logGetSelectedDietRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetDietRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetDietRecipes.logger.info("------------------Enter get Recipes By All Diet Types---------------")
            recipeslst = recipeModel.get_recipes_by_diet_type()
            logGetDietRecipes.logger.info("Get Recipe By Diet success")
            logGetDietRecipes.logger.info("------------------End of Get Recipes By All Diet Types---------------")
            return {"recipes": recipeslst}, 200
            # return jsonify({ "error": "Email address already in use" }), 400

        except Exception as ex:
            logGetDietRecipes.logger.error("Error processing the request")
            logGetDietRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetPopularRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetPopularRecipes.logger.info("------------------Enter get Recipes By Popularity---------------")
            recipeslst = recipeModel.get_recipes_by_popularity()
            logGetPopularRecipes.logger.info("Get Recipe By Popularity success")
            logGetPopularRecipes.logger.info("------------------End of Get Recipes By Popularity---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetPopularRecipes.logger.error("Error processing the request")
            logGetPopularRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetPopularRatedRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetPopularRatedRecipes.logger.info("------------------Enter get Recipes By Popularity and RAting Type---------------")
            rcp = request.get_json()
            csn = rcp.get('rating')
            recipeslst = recipeModel.get_recipes_by_rating(csn)
            logGetPopularRatedRecipes.logger.info("Get Recipe By Popularity By Rating success")
            logGetPopularRatedRecipes.logger.info("------------------End of Get Recipes By Popularity and Rating Type---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetPopularRatedRecipes.logger.error("Error processing the request")
            logGetPopularRatedRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


# class GetPopularRatedRecipesApi(Resource):
#     def get(self):
#         try:
#             signUp.logger.info("------------------Enter get REcipes By Cusine Type---------------")
#             rcp = request.get_json()
#             csn = rcp.get('rating')
#             recipeslst = recipeModel.get_recipes_by_rating(csn)
#             #print("controller")
#             #print(recipeslst)
#             signUp.logger.info("Inserted docuemnt successfully")
#             signUp.logger.info("------------------End of Get REcipes By Cusine Type---------------")
#             return  {"recipes":json.dumps(recipeslst)}, 200
#             #return jsonify({ "error": "Email address already in use" }), 400

#         except Exception as ex:
#             signUp.logger.error("Error processing the request")
#             raise ex
#             #return {'error': 'Error processing the request'}, 400

class GetPopularReviewedRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetPopularReviewRecipes.logger.info("------------------Enter get Recipes By Popularity and Reviews Type---------------")
            recipeslst = recipeModel.get_recipes_by_review()
            logGetPopularReviewRecipes.logger.info("Get Recipe By Popularity By Review success")
            logGetPopularReviewRecipes.logger.info("------------------End of Get REcipes By Popularity and Reviews Type---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetPopularReviewRecipes.logger.error("Error processing the request")
            logGetPopularReviewRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetRecipesByCookingTimeApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetCookingRecipes.logger.info("------------------Enter get Recipes By Cooking Time---------------")
            recipeslst = recipeModel.get_recipes_by_cooking_time()
            logGetCookingRecipes.logger.info("Get Recipe By Cooking Time success")
            logGetCookingRecipes.logger.info("------------------End of Get REcipes By Cooking Time---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetCookingRecipes.logger.error("Error processing the request")
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetRecipesBySelectedCookingTimeApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetSelectedCookingRecipes.logger.info("------------------Enter Get Recipes By Selected Cooking Time---------------")
            rcp = request.get_json()
            ct = rcp.get('cookingtime')
            recipeslst = recipeModel.get_recipes_by_selected_cooking_time(ct)
            logGetSelectedCookingRecipes.logger.info("Get Recipe By Selected Cooking Time success")
            logGetSelectedCookingRecipes.logger.info("------------------End of Get Recipes By Selected Cooking Time---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetSelectedCookingRecipes.logger.error("Error processing the request")
            # raise ex
            logGetSelectedCookingRecipes.logger.error(ex)
            return {'error': 'Error processing the request'}, 400


class GetRecipesByIngredientApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetSelectedIngredRecipes.logger.info("------------------Enter Get Recipes By Selected Ingredient Type---------------")
            rcp = request.get_json()
            ct = rcp.get('ingredient')
            recipeslst = recipeModel.get_recipes_by_selected_ingredient(ct)
            logGetSelectedIngredRecipes.logger.info("Get Recipe By Selected Ingredient success")
            logGetSelectedIngredRecipes.logger.info("------------------End of Get Recipes By Selected Ingredient Type---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetSelectedIngredRecipes.logger.error("Error processing the request")
            logGetSelectedIngredRecipes.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetRecipesByIngredientsApi(Resource):
    @cross_origin()
    def post(self):
        try:
            logGetIngredRecipes.logger.info("------------------Enter Get Recipes By Ingredients List---------------")
            rcp = request.get_json()
            #print("j")
            #print(rcp)
            ct = rcp.get('ingredients')
            user = rcp.get('token')
            recipeslst = recipeModel.get_recipes_by_selected_ingredients(ct,user)

            logGetIngredRecipes.logger.info("Get Recipe By Selected Ingredients success")
            logGetIngredRecipes.logger.info("------------------End of Get REcipes By Ingredients List---------------")
            #data = {"recipes":recipeslst}
            #print(data["recipes"])
             
            return {"recipes":recipeslst}, 200
        except Exception as ex:
            logGetIngredRecipes.logger.error("Error processing the request")
            logGetIngredRecipes.logger.error(ex)
            raise(ex)
            return {'error': 'Error processing the request'}, 400


class UpdateRating(Resource):
    @cross_origin()
    def post(self):
        try:
            logUpdateRating.logger.info("------------------Enter Update Rating---------------")
            rcp = request.get_json()
            recipeslst = recipeModel.update_rating(rcp)
            logUpdateRating.logger.info("Updated Recipe Rating Successfully")
            logUpdateRating.logger.info("------------------End of Update Recipe Rating---------------")
            # return  jsonify({"message":"Updated rating successfully"}), 200
            return {'message': 'Updated rating successfully'}, 200
        except Exception as ex:
            logUpdateRating.logger.error("Error processing the request")
            # raise ex
            logUpdateRating.logger.error(ex)
            return {'error': 'Error processing the request'}, 400


class UpdateReview(Resource):
    @cross_origin()
    def post(self):
        try:
            logUpdateReview.logger.info("------------------Enter Update Recipe Review---------------")
            rcp = request.get_json()
            recipeslst = recipeModel.update_review(rcp)
            logUpdateReview.logger.info("Updated Recipe Review successfully")
            logUpdateReview.logger.info("------------------End of Update Recipe Review---------------")
            return {'message': 'Updated review successfully'}, 200
        except Exception as ex:
            logUpdateReview.logger.error("Error processing the request")
            logUpdateReview.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class SearchRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logSearchRecipe.logger.info("------------------Enter Search Recipes By Title---------------")
            rcp = request.get_json()
            title = rcp['titles']
            recipeslst = recipeModel.get_recipes_by_title(title)
            logSearchRecipe.logger.info("Searched docuemnt successfully")
            logSearchRecipe.logger.info("------------------End of Search Recipes By Title---------------")
            return {'recipes': recipeslst}, 200
        except Exception as ex:
            logSearchRecipe.logger.error("Error processing the request")
            # raise ex
            logSearchRecipe.logger.ex(ex)
            return {'error': 'Error processing the request'}, 400

class GetVeganRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetCookingRecipes.logger.info("------------------Enter get Vegan Recipes---------------")
            recipeslst = recipeModel.get_vegan_recipes()
            logGetCookingRecipes.logger.info("Get Vegan Recipes success")
            logGetCookingRecipes.logger.info("------------------End of Get Vegan Recipes---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetCookingRecipes.logger.error("Error processing the request")
            # raise ex
            return {'error': 'Error processing the request'}, 400
            #re_train_model

class GetNonVeganRecipesApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetCookingRecipes.logger.info("------------------Enter Get Non Vegan Recipes---------------")
            recipeslst = recipeModel.get_non_vegan_recipes()
            logGetCookingRecipes.logger.info("Get Non Vegan Recipes success")
            logGetCookingRecipes.logger.info("------------------End of Get Non Vegan Recipes---------------")
            return {"recipes": recipeslst}, 200
        except Exception as ex:
            logGetCookingRecipes.logger.error("Error processing the request")
            # raise ex
            return {'error': 'Error processing the request'}, 400

class ReTrainModelApi(Resource):
    @cross_origin()
    def get(self):
        try:
            logGetCookingRecipes.logger.info("------------------Enter Retrain ML model---------------")
            recipeModel.re_train_model()
            logGetCookingRecipes.logger.info("Retrain ML model success")
            logGetCookingRecipes.logger.info("------------------End of Retrain ML model---------------")
            return "Re-trained model Successfully", 200
        except Exception as ex:
            logGetCookingRecipes.logger.error("Error processing the request")
            raise ex
            return {'error': 'Error processing the request'}, 400
