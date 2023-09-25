import csv
import pandas as pd
from sqlalchemy import  String, Integer, DateTime
from db_auth import connecty_stuff

# Define the path to your CSV file
csv_file_path = 'data/fsq_export_modified.csv'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, header=0)

engine = connecty_stuff()

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
table_name = 'FoodSkillsQuestionnaire'

user_csv_data = []
user_csv_file = "data/qchef_study2_participants_and_aliases.csv"
#Open the CSV file and read the data
with open(user_csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user_csv_data.append(row)

user_csv_dict = {row["\ufeffUID"]:row for row in user_csv_data}
email_lookup = {}
for k,v in user_csv_dict.items():
    email_lookup[v["Account Email"]] = k
    if len(v["Alias 1"]):
        email_lookup[v["Alias 1"]] = k
    if len(v["Alias 2"]):
        email_lookup[v["Alias 2"]] = k



for c,d in zip(df.columns.tolist(),fields.keys()):
    print(c+" --> "+d)
    df.rename(columns={c:d},inplace=True)

#Replace the emails in the above export with the actual user IDs
for index,row in df.iterrows():
    try:
        df.at[index,"User_ID"] = email_lookup[row["User_ID"]]
    except:
        print("Failed to substitute email address " + row["User_ID"])

print(df)
fields['FSQ_ID'] = Integer()
df["FSQ_ID"] = range(len(df))
df.set_index("FSQ_ID", inplace=True)
fields['survey_iteration'] = Integer()
df["survey_iteration"] = None

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=True, dtype=fields)