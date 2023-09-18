import pandas as pd
from sqlalchemy import create_engine
from db_auth import *

# Define the path to your CSV file
csv_file_path = 'data/fsq_export_modified.csv'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, header=0)

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

fields = { 
          'timestamp': "TIMESTAMP", 
          'User_ID': "VARCHAR(64)",
          'q1_bbd': "VARCHAR(40)", 
          'q2_grocery': "VARCHAR(40)", 
          'q3_buyvarveg': "VARCHAR(40)", 
          'q4_confbudggroc': "INT",
          'q5_confmealplan': "INT", 
          'q6_confselectveg': "INT", 
          'q7_confreadlabel': "INT", 
          'q8_planmealathome': "INT", 
          'q9_confadjustrecipe': "INT", 
          'q10_timesownbrekkie': "VARCHAR(40)", 
          'q11_timesownlunch': "VARCHAR(40)", 
          'q12_timesowndinner': "VARCHAR(40)", 
          'q13_oftenmealsbalanced': "VARCHAR(40)", 
          'q14_abilitytoprepare': "VARCHAR(160)", 
          'q15_confknives': "INT", 
          'q16_confpeel': "INT", 
          'q17_confvegprep': "INT", 
          'q18_conflegume': "INT", 
          'q19_confprepbasic': "INT", 
          'q20_confrecipe': "INT", 
          'q21_confboil': "INT", 
          'q22_conffry': "INT",       
          'q23_confbake': "INT", 
          'q24_confspice': "INT", 
          'q25_confnew': "INT"
          }

# Replace 'your_table_name' with the name of your database table
table_name = 'FoodSkillsQuestionnaire_test'

for c,d in zip(df.columns.tolist(),fields.keys()):
    print(c+" --> "+d)
    df.rename(columns={c:d},inplace=True)
print(df)
fields['FSQ_ID'] = "INT AUTO_INCREMENT PRIMARY KEY"
df["FSQ_ID"] = None
fields['survey_iteration'] = "INT"
df["survey_iteration"] = None

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=False)#, dtype=fields)