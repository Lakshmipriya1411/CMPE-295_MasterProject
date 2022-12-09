from api.database.model import ingredients
from flask_restful import Resource
from api.logging.logger import ingredsFreq, ingreds
import json
from flask_cors import cross_origin

ingredients = ingredients.IngredientsModel()


class GetingredientsApi(Resource):
    @cross_origin()
    def get(self):
        try:
            ingreds.logger.info("------------------Enter get Ingredients---------------")
            ingredient = ingredients.get_ingredients()
            ingreds.logger.info("Fetchings Ingredients successfully")
            ingreds.logger.info("------------------End of Get Ingredients---------------")
            return {"ingredients": ingredient}, 200
        except Exception as ex:
            ingreds.logger.error("Error processing the request")
            ingreds.logger.error(ex)
            # raise ex
            return {'error': 'Error processing the request'}, 400


class GetIngredientFrequencyMapApi(Resource):
    @cross_origin()
    def get(self):
        try:
            ingredsFreq.logger.info("------------------Enter get Ingredients FrequencyMap---------------")
            ingreds = ingredients.get_ingredients_frequency_map()
            del ingreds[0]['_id']
            ingredsFreq.logger.info("Inserted docuemnt successfully")
            ingredsFreq.logger.info("------------------End of Get Ingredients Frequency Map---------------")
            return ingreds, 200

        except Exception as ex:
            ingredsFreq.logger.error("Error processing the request")
            ingredsFreq.logger.error(ex)
            raise ex
