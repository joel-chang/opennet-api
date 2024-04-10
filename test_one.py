import random
import pytest

from cat_facts_api.api_models.FactList import FactList
from cat_facts_api.api_models.Fact import Fact
from cat_facts_api.api_models.FactById import FactByID
from cat_facts_api.exceptions import CatApiException
from cat_facts_api.rest_adapter import RestAdapter


@pytest.fixture(name="default_cat")
def fixture_default_cat():
    catapi = RestAdapter('cat-fact.herokuapp.com')
    return catapi


def test_default_call(default_cat):
    res = default_cat.get('facts')
    fact_list = FactList.from_list(res.data)
    assert len(fact_list.items) == 5


def test_default_type_is_cat(default_cat):
    params = {'amount': random.randint(2, 500)}
    res = default_cat.get('facts/random', ep_params=params)
    fact_list = FactList.from_list(res.data)

    for fact in fact_list.items:
        assert fact.type == 'cat'


def test_type_is_dog(default_cat):
    params = {'animal_type': 'dog', 'amount': random.randint(2, 500)}
    res = default_cat.get('facts/random', ep_params=params)
    fact_list = FactList.from_list(res.data)

    for fact in fact_list.items:
        print(fact)
        assert fact.type == 'dog'


def test_multiple_types(default_cat):
    # this one is very example-y (mock db, build data? but random)
    params = {'animal_type': 'dog,cat,horse', 'amount': 500}
    res = default_cat.get('facts/random', ep_params=params)
    fact_list = FactList.from_list(res.data)

    dog_count = 0
    horse_count = 0
    cat_count = 0
    for fact in fact_list.items:
        assert fact.type in ['dog', 'cat', 'horse']
        if fact.type == 'dog':
            dog_count += 1
        elif fact.type == 'cat':
            cat_count += 1
        elif fact.type == 'horse':
            horse_count += 1

    assert dog_count > 0
    assert horse_count > 0
    assert cat_count > 0


def test_nonexisting_animal_types(default_cat):
    params = {
        'animal_type': 'pizza,car,Elon,Homelander',
        'amount': random.randint(
            2,
            500)}
    res = default_cat.get('facts/random', ep_params=params)
    fact_list = FactList.from_list(res.data)

    assert len(fact_list.items) == 0


def test_eq_1_returns_single_fact_not_list():
    pass


def test_gte_2_lte_500(default_cat):
    random_length = random.randint(2, 500)
    params = {'animal_type': 'cat', 'amount': random_length}
    res = default_cat.get('facts/random', ep_params=params)
    fact_list = FactList.from_list(res.data)
    assert len(fact_list.items) == random_length


def test_amount_gte_501_not_allowed(default_cat, capsys):
    # pytest's capsys fixture
    # fuzz
    params = {'animal_type': 'cat',
              'amount': random.randint(501, 100000000000)}
    try:
        default_cat.get('facts/random', ep_params=params)
    except CatApiException as e:
        print(e)
    captured_err = capsys.readouterr()
    assert captured_err.out == '405: Method Not Allowed\n'


def test_amount_lte_0_returns_empty_list(default_cat):
    params = {'animal_type': 'cat',
              'amount': random.randint(-10000000000000, 0)}
    try:
        res = default_cat.get('facts/random', ep_params=params)
    except CatApiException as e:
        print(e)
    assert res.data == []


def test_random_then_by_id(default_cat):
    # api abstraction is very barebones and models aren't well written (lazy)
    # when querying a fact by :id and by /random, the resp structure is
    # different (technically different endpoints, same dataclass + optional?)
    params = {'amount': 1}
    res0 = default_cat.get('facts/random', ep_params=params)
    fact0 = Fact.from_dict(res0.data)

    res1 = default_cat.get(f'facts/{fact0.id}')
    fact1 = FactByID.from_dict(res1.data)

    assert fact0 == fact1  # override __eq__, debatable
