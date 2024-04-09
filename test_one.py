import pytest
import random

from cat_facts_api.api_models.FactList import FactList
from cat_facts_api.rest_adapter import RestAdapter


@pytest.fixture
def default_cat():
    catapi = RestAdapter('cat-fact.herokuapp.com')
    return catapi

def test_default_call(default_cat):
    res = default_cat.get('facts')
    fact_list = FactList.from_list(res.data)
    assert len(fact_list.items) == 5

def test_random_list_length(default_cat):
    random_length = random.randint(3, 30)
    params = {'animal_type': 'cat', 'amount': random_length}
    res = default_cat.get('facts/random', ep_params=params)

def test_list_length_without_specifying_animal_type(default_cat):
    params = {'amount': ''}