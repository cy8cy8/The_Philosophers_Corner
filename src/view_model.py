import tkinter as tk
import json
from model import Util, data_src
import os

class ViewModel(Util):
    def __init__(self, model):
        self.model = model
        self.categories:tuple = self.get_categories()
        self.category_var = tk.StringVar(value="")
        self.is_modified = False  # Flag to track modifications

    def display_all_wisdom(self):
        return self.model.get_all_wisdom()
    
    def display_wisdom_from_a_category(self, category):
        return self.get_wisdom_from_a_category(category)
    
    def insert_new_wisdom(self, category:str, new_wisdom:str) -> None:
        with open(data_src, "r") as f:
            data = json.load(f)
        if category in data:
            data[category].append(new_wisdom)
        else:
            data[category] = [new_wisdom]
            self.categories = self.get_categories()
        with open(data_src, "w") as f:
            # f.seek(0)
            json.dump(data, f, indent=4)
        self.is_modified = True