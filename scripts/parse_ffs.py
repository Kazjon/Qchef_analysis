import csv
import pandas as pd
from datetime import datetime
from sqlalchemy import  String, Integer, DateTime
from db_auth import connecty_stuff

# Define the path to your CSV file
csv_file_path = 'data/ffs_export.csv'

# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, header=0)

engine = connecty_stuff()

fields = { 
          'timestamp': DateTime(), 
          'User_ID': String(64),
          'iteration': Integer(), 
          'a1_beercider': String(40), 
          'a2_spirits': String(40), 
          'a3_wine': String(40), 
          'd1_milk': String(40), 
          'd2_butter': String(40),  
          'd3_cream': String(40), 
          'd4_cheese': String(40), 
          'd5_yoghurt': String(40), 
          'd6_eggs': String(40), 
          'd7_otherdairy': String(40),
          'd8_dairysubs': String(40),
          'f1_apples': String(40),
          'f2_bananas': String(40),
          'f3_citrus': String(40),
          'f4_pears': String(40),
          'f5_grapes': String(40),
          'f6_mangos': String(40),
          'f7_melons': String(40),
          'f8_berries': String(40),
          'f9_stonefruit': String(40),
          'f10_otherfruit': String(40),
          'f11_driedfruit': String(40),
          'c1_flour': String(40),
          'c2_corn': String(40),
          'c3_oats': String(40),
          'c4_rice': String(40),
          'c5_pasta': String(40),
          'c6_bread': String(40),
          'c7_flatbread': String(40),
          'c8_pizza': String(40),
          'c9_bakedgoods': String(40),
          'c10_othergrains': String(40),
          'p1_whitefish': String(40), 
          'p2_oilyfish': String(40), 
          'p3_crustaceans': String(40), 
          'p4_squid': String(40), 
          'p5_molluscs': String(40), 
          'p6_otherseafood': String(40),
          'p7_beef': String(40), 
          'p8_chicken': String(40), 
          'p9_pork': String(40), 
          'p10_lamb': String(40),
          'p11_duck': String(40), 
          'p12_sausages': String(40), 
          'p13_curedmeat': String(40), 
          'p14_organs': String(40), 
          'p15_meatsubs': String(40), 
          'p16_othermeats': String(40), 
          'o1_teacoffee': String(40), 
          'o2_nuts': String(40), 
          'o3_seeds': String(40), 
          'o4_coconut': String(40), 
          'o5_soy': String(40), 
          'o6_oils': String(40), 
          'o7_proteinpowder': String(40), 
          's1_sugar': String(40), 
          's2_honey': String(40), 
          's3_maple': String(40), 
          's4_othersyrups': String(40), 
          's5_jam': String(40), 
          's6_chocolate': String(40), 
          's7_icecream': String(40), 
          's8_soda': String(40), 
          's9_othersweets': String(40), 
          's10_otherdesserts': String(40), 
          'v1_lettuce': String(40), 
          'v2_spinach': String(40), 
          'v3_rocket': String(40), 
          'v4_kale': String(40), 
          'v5_seaweed': String(40), 
          'v6_otherleafygreens': String(40), 
          'v7_cruciferous': String(40), 
          'v8_beans': String(40), 
          'v9_lentils': String(40), 
          'v10_peas': String(40), 
          'v11_garlic': String(40), 
          'v12_ginger': String(40), 
          'v13_chili': String(40), 
          'v14_mushrooms': String(40), 
          'v15_leek': String(40), 
          'v16_onions': String(40), 
          'v17_potatoes': String(40), 
          'v18_sweetpotatoes': String(40),
          'v19_pumpkin': String(40), 
          'v20_othertubers': String(40), 
          'v21_tomatoes': String(40), 
          'v22_avocado': String(40), 
          'v23_asparagus': String(40), 
          'v24_capsicum': String(40), 
          'v25_zucchini': String(40), 
          'v26_eggplant': String(40),
          'v27_fennel': String(40),
          'v28_olives': String(40),
          'v29_cucumbers': String(40),
          'v30_pickledveg': String(40),
          'v31_otherveg': String(40)
          }

# Replace 'your_table_name' with the name of your database table
table_name = 'FoodFrequencySurvey'

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

date_format = "%m/%d/%Y %H:%M:%S"

#Replace the emails in the above export with the actual user IDs and then convert the datetime strings into objects
for index,row in df.iterrows():
    try:
        df.at[index,"User_ID"] = email_lookup[row["User_ID"]]
    except:
        print("Failed to substitute email address " + row["User_ID"])
    df.at[index,"timestamp"] = datetime.strptime(row["timestamp"],date_format)

print(df["timestamp"])
fields['FFS_ID'] = Integer()
df["FFS_ID"] = range(len(df))
df.set_index("FFS_ID", inplace=True)

# Write the DataFrame to the database table
df.to_sql(table_name, con=engine, if_exists='replace', index=True, dtype=fields)