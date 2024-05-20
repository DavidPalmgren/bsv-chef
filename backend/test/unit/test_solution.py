import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController
from enum import Enum


class Diet(Enum):
    NORMAL = 1
    VEGETARIAN = 2
    VEGAN = 3

# add your test case implementation here
@pytest.mark.unit
def test():
    pass

@pytest.fixture
def mocked_controller():
    dao = MagicMock()
    return RecipeController(dao)


# 1 , 2 ,3 take best
@pytest.mark.parametrize('diet, expected', [
    (Diet.NORMAL, "banana_milk"),
    (Diet.VEGAN, "banana_milk"),
    (Diet.VEGETARIAN, "banana_milk")
])
def test_get_recipe_valid_take_best(mocked_controller, diet, expected):
    
    expected_return = expected
    readiness_of_recepies = {
        expected_return: 0.1,
        "potatis": 0.01,
        "frölunda": 0.033
    }
    take_best = True
    
    mocked_controller.get_readiness_of_recipes = MagicMock(return_value= readiness_of_recepies)
    res = mocked_controller.get_recipe(diet, take_best)
    assert res == expected_return


# 4, 5 ,6 take random
@pytest.mark.parametrize('diet, recepies', [
    (Diet.NORMAL, ["banana_milk", "potatis", "frölunda"]),
    (Diet.VEGAN, ["banana_milk", "potatis", "frölunda"]),
    (Diet.VEGETARIAN, ["banana_milk", "potatis", "frölunda"])
])
def test_get_recipe_valid_take_random(mocked_controller, diet, recepies):
    
    expected_return = recepies
    readiness_of_recepies = {
        "frölunda": 0.5
    }
    take_best = False
    
    
    mocked_controller.get_readiness_of_recipes = MagicMock(return_value= readiness_of_recepies)
    res = mocked_controller.get_recipe(diet, take_best)
    assert res in expected_return

# 7, we test that none is returned if no readiness val at or below 0.1
@pytest.mark.parametrize('diet, recepies', [
    (Diet.NORMAL, {"banana_milk": 0.09,"potato_milk":0.09, "choklad": 0.01}),
    (Diet.VEGAN, {"banana_milk": 0.09,"potato_milk":0.09, "choklad": 0.01}),
    (Diet.VEGETARIAN, {"banana_milk": 0.09,"potato_milk":0.09, "choklad": 0.01})
])
def test_get_recipe_invalid_none(mocked_controller, diet, recepies):
    take_best = False #doesnt matter
    mocked_controller.get_readiness_of_recipes = MagicMock(return_value=recepies)
    res = mocked_controller.get_recipe(diet, take_best)
    
    assert res == None

# {
#     "name": "Whole Grain Bread",
#     "diets": [
#         "normal", "vegetarian", "vegan"
#     ],
#     "ingredients": {
#         "Flour": 500,
#         "Walnuts": 20,
#         "Yeast": 1,
#         "Salt": 10,
#         "Vinegar": 30
#     }
# }