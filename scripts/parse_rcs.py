import csv
import pandas as pd
from datetime import datetime
from sqlalchemy import  String, Integer, DateTime
from db_auth import connecty_stuff

# Define the path to your CSV file
csv_file_path = 'data/Q-chef Study II RQS.csv'

# Use pandas to read the CSV file into a DataFrame
raw_df = pd.read_csv(csv_file_path, header=0)

engine = connecty_stuff()

fields = { 
          'timestamp': DateTime(), 
          'User_ID': String(64),
          'Recipe_ID': String(64),
          "_title": Integer(),
          'q1_wantknowtaste': Integer(), 
          'q2_fascinating': Integer(), 
          'q3_trymore': Integer(), 
          'q4_learnmore': Integer(), 
          'q5_notcurious': Integer(),
          "_q6": Integer(),
          "_q7": Integer(),
          "_q8": Integer(),
          "_q9": Integer(),
          "_q10": Integer()
          }

# Replace 'your_table_name' with the name of your database table
table_name = 'RecipeCuriosityQuestionnaire'

df = pd.DataFrame()

for c,d in zip(raw_df.columns.tolist(),fields.keys()):
    print(c+" --> "+d)
    if not d[0] == "_":
        df[d] = raw_df[c]


date_format = "%m/%d/%Y %H:%M:%S"

#Replace the emails in the above export with the actual user IDs and then convert the datetime strings into objects
for index,row in df.iterrows():
    df.at[index,"timestamp"] = datetime.strptime(row["timestamp"],date_format)

print(df)
fields['RCQ_ID'] = Integer()
df["RCQ_ID"] = range(len(df))
df.set_index("RCQ_ID", inplace=True)

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=True, dtype=fields)