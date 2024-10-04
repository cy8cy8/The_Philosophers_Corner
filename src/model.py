import json
from random import randint
import os

# Update data_src to point to a local path
data_src = os.path.join(os.path.dirname(__file__), 'wisdom.json')

class Util:
    # Default constructor used without __init__(). Set up __init__ if there are attributes.
    def get_all_wisdom(self) -> str:
        with open(data_src, "r") as f:
            data = json.load(f)
            all_keys = list(data.keys())
            rand_int = randint(0, len(data)-1)
            rand_category_index:str = all_keys[rand_int]
            result = data[rand_category_index]
            len_result_list = len(data[rand_category_index])
            return result[randint(0, len_result_list-1)]
        
    def get_categories(self):
        with open(data_src, "r") as f:
            data = json.load(f)
            return tuple(data.keys())
        
    def get_wisdom_from_a_category(self, category:str) -> str:
        with open(data_src, "r") as f:
            all_wisdom = json.load(f)
        wisdom_list = all_wisdom[category]
        return wisdom_list[randint(0, len(wisdom_list)-1)]