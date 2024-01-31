import os
import json
eating = []
not_eating = []
for i in os.listdir(f'data\eating'):
    dictionary = dict()
    dictionary["name"] = i.split(".")[0]
    dictionary["path"] = f'data\eating\{i}'

with open("data"