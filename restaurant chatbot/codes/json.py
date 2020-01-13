# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:02:48 2020

@author: chest
"""

import json
import os
import pandas as pd

#Change to your directory
os.chdir(r"C:\Users\chest\Desktop\Projects\Restaurant Chatbot\data")

def file_lbl(directory, encoding):
    file = open(directory, "r", encoding=encoding)
    storage = []
    while True:
        line = file.readline()
        if line:
            json_data = json.loads(line)
            storage.append(json_data)
        if not line:
            file.close()
            break
    return storage

json_list = file_lbl("yelp_review.json", "utf8")

review_df = pd.DataFrame(json_list)

review_df.to_pickle(r"./review_df.pkl")

# use this code to read pickle
test = pd.read_pickle(r"./review_df.pkl")