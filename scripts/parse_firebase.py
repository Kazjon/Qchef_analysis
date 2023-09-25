import json,csv

import pandas as pd
from sqlalchemy import String, Integer, DateTime, JSON
from db_auth import connecty_stuff

# Replace 'your_file.json' with the path to your JSON file
json_file = 'data/q-chef-export.json'

# Load the JSON data from the file
with open(json_file, 'r') as file:
    data = json.load(file)

csv_data = []
csv_file = "data/qchef_study2_participants_and_aliases.csv"
#Open the CSV file and read the data
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        csv_data.append(row)

csv_dict = {row["\ufeffUID"]:row for row in csv_data}

users_dict = {}
#Extract the relevant user fields from data["__collections__"]["users"] and populate a pandas dataframe with them
for uid,user_collection in data["__collections__"]["users"].items():
    if uid in csv_dict.keys():
        user_dict = {
            "Name": csv_dict[uid]["Full Name"],
            "Email": csv_dict[uid]["Account Email"],
            "Email_Alias_1": csv_dict[uid]["Alias 1"],
            "Email_Alias_2": csv_dict[uid]["Alias 2"],
            "Experimental_Group": user_collection["group"],
            "Served_Recipes": user_collection["servedRecipes"],
            "Picked_Recipes": user_collection["pickedRecipes"],   
        }
        users_dict[uid] = user_dict

#Define a dictionary with the field datatypes for the Users table
user_fields = {
        "User_ID": String(64),
        "Name": String(64),
        "Email": String(64),
        "Email_Alias_1": String(64),
        "Email_Alias_2": String(64),
        "Experimental_Group": Integer(),
        "Served_Recipes": JSON(),
        "Picked_Recipes": JSON(),   
    }
#Do all the database connecty stuff (maybe save this as a function so we don't have to do it every time?)
engine = connecty_stuff()

#Pandify 
df = pd.DataFrame.from_dict(users_dict, orient="index")
df.index.name = "User_ID"

#Yeet the dataframe into the database
df.to_sql("Users", con=engine, if_exists='replace', index=True, dtype=user_fields)