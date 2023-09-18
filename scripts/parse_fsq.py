import pandas as pd
from sqlalchemy import create_engine, String, Integer, DateTime
from db_auth import *

# Define the path to your CSV file
csv_file_path = 'data/fsq_export_modified.csv'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, header=0)

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

fields = { 
          'timestamp': DateTime(), 
          'User_ID': String(64),
          'q1_bbd': String(40), 
          'q2_grocery': String(40), 
          'q3_buyvarveg': String(40), 
          'q4_confbudggroc': Integer(),
          'q5_confmealplan': Integer(), 
          'q6_confselectveg': Integer(), 
          'q7_confreadlabel': Integer(), 
          'q8_planmealathome': Integer(), 
          'q9_confadjustrecipe': Integer(), 
          'q10_timesownbrekkie': String(40), 
          'q11_timesownlunch': String(40), 
          'q12_timesowndinner': String(40), 
          'q13_oftenmealsbalanced': String(40), 
          'q14_abilitytoprepare': String(160), 
          'q15_confknives': Integer(), 
          'q16_confpeel': Integer(), 
          'q17_confvegprep': Integer(), 
          'q18_conflegume': Integer(), 
          'q19_confprepbasic': Integer(), 
          'q20_confrecipe': Integer(), 
          'q21_confboil': Integer(), 
          'q22_conffry': Integer(),       
          'q23_confbake': Integer(), 
          'q24_confspice': Integer(), 
          'q25_confnew': Integer()
          }

# Replace 'your_table_name' with the name of your database table
table_name = 'FoodSkillsQuestionnaire_test'

for c,d in zip(df.columns.tolist(),fields.keys()):
    print(c+" --> "+d)
    df.rename(columns={c:d},inplace=True)
print(df)
fields['FSQ_ID'] = Integer()
df["FSQ_ID"] = range(len(df))
df.set_index("FSQ_ID", inplace=True)
fields['survey_iteration'] = Integer()
df["survey_iteration"] = None

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=False, dtype=fields)