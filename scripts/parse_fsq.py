import pandas as pd
from sqlalchemy import create_engine
from db_auth import *

# Define the path to your CSV file
csv_file_path = 'data/fsq_export_modified.csv'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, header=0)

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Replace 'your_table_name' with the name of your database table
table_name = 'FoodSkillsQuestionnaire_test'

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=False)