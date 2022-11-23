from api.resources.auth import SignupApi,SignInApi,SignoutApi
from api.resources.ingredients import GetingredientsApi,GetIngredientFrequencyMapApi
from api.resources.recipes import GetRecipesApi,GetSelectedRecipeApi,GetCuisineRecipesApi,GetDietRecipesApi,GetSelectedDietRecipesApi,GetPopularRecipesApi,GetPopularRatedRecipesApi
from api.resources.recipes import GetPopularReviewedRecipesApi,GetRecipesByCookingTimeApi,GetRecipesBySelectedCookingTimeApi,GetRecipesByIngredientApi,GetRecipesByIngredientsApi
from api.resources.recipes import UpdateRating,UpdateReview,SearchRecipesApi,GetVeganRecipesApi,GetNonVeganRecipesApi,ReTrainModelApi
from http import HTTPStatus
from flasgger import swag_from


def initialize_routes(api):
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(SignInApi, '/api/auth/signin')
    api.add_resource(SignoutApi, '/api/auth/signout')
    api.add_resource(GetingredientsApi, '/api/ingredients')
    api.add_resource(GetIngredientFrequencyMapApi,'/api/ingredients/frequency')
    api.add_resource(GetRecipesApi,'/api/recipes/cuisine')
    api.add_resource(GetSelectedRecipeApi,'/api/recipes/cuisine')
    api.add_resource(GetCuisineRecipesApi,'/api/recipes/cuisine/type')
    api.add_resource(GetDietRecipesApi,'/api/recipes/diet')
    api.add_resource(GetSelectedDietRecipesApi,'/api/recipes/diet/type')
    api.add_resource(GetPopularRecipesApi,'/api/recipes/popular')
    api.add_resource(GetPopularRatedRecipesApi,'/api/recipes/popular/rating')
    api.add_resource(GetPopularReviewedRecipesApi,'/api/recipes/popular/review')
    api.add_resource(GetRecipesByCookingTimeApi,'/api/recipes/cookingtime')
    api.add_resource(GetRecipesBySelectedCookingTimeApi,'/api/recipes/cookingtime/time')
    api.add_resource(GetRecipesByIngredientApi,'/api/recipes/ingredient/type')
    api.add_resource(GetRecipesByIngredientsApi,'/api/recipes/ingredients')
    api.add_resource(UpdateRating,'/api/recipes/rating')
    api.add_resource(UpdateReview,'/api/recipes/review')
    api.add_resource(SearchRecipesApi,'/api/recipe')
    api.add_resource(GetVeganRecipesApi,'/api/vegan')
    api.add_resource(GetNonVeganRecipesApi,'/api/nonvegan')
    api.add_resource(ReTrainModelApi,"/api/retrain")
    
