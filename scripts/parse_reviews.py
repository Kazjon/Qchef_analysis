import csv
import pandas as pd
from datetime import datetime
from sqlalchemy import  String, Integer, DateTime
from db_auth import connecty_stuff

# Define the path to your CSV file
csv_file_path = 'data/qchef_reviews.csv'

# Use pandas to read the CSV file into a DataFrame
raw_df = pd.read_csv(csv_file_path, header=0, delimiter=";")

engine = connecty_stuff()

#structure of reviews file: user_id;recipe_id;cook_rating;taste_rating;familiarity_rating:why;how;group

fields = { 
          'User_ID': String(64),
          'Recipe_ID': String(64),
          "cook_rating": Integer(),
          'taste_rating': Integer(), 
          'fam_rating': Integer(), 
          'why': String(1024), 
          'how': String(1024), 
          '_group': Integer(),
          }

# Replace 'your_table_name' with the name of your database table
table_name = 'RecipeReviews'

df = pd.DataFrame()

for c,d in zip(raw_df.columns.tolist(),fields.keys()):
    print(c+" --> "+d)
    if not d[0] == "_":
        df[d] = raw_df[c]

print(df)
fields['Review_ID'] = Integer()
df["Review_ID"] = range(len(df))
df.set_index("Review_ID", inplace=True)

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=True, dtype=fields)

#After running this on the ever-lovely PhPMyAdmin, we used the following query to get it all back out again:
