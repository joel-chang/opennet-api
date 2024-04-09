import json
from api_models.FactList import FactList
from rest_adapter import RestAdapter
from api_models.Fact import Fact

catapi = RestAdapter('cat-fact.herokuapp.com')
params = {'animal_type': 'cat', 'amount': 1}
catlist = catapi.get('facts/random', ep_params=params)

# print(json.dumps(catlist))
print(json.dumps(catlist.data, indent=4))
print(FactList.from_single(catlist.data))
# pprint.pprint(Fact.from_dict(catlist.data))

# pprint.pprint(catlist.status_code)
# pprint.pprint(catlist.message)
# pprint.pprint(Fact.from_dict(catlist.data[0]))