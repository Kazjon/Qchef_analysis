import pandas as pd
import numpy as np

filename = 'data/RCQ_export_fixed.csv'

df = pd.read_csv(filename)

#temporarily axe jbat and tbls, whose data is a bit screwy
df = df[df["User_ID"] != "JbaTvCAyhyNVVJgGMLi4wAIOcSw2"]
df = df[df["User_ID"] != "TblSvuNZG6TFuCe57LqIHDzyArJ3"]

for column in ["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_notcurious","Experimental_Group"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df.dropna(subset=["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_notcurious"], inplace=True)

df["q5_flipped"] = 6 - df["q5_notcurious"]
df["curiosity_average"] = df[["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_flipped"]].mean(axis=1)

print(df.head())

from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

pairs = [(0,1), (0,2), (1,2)]
for column in ["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_notcurious","curiosity_average"]:
    for pair in pairs:
        pair1 = df[df["Experimental_Group"] == pair[0]][column]
        pair2 = df[df["Experimental_Group"] == pair[1]][column]
        t_stat, p_value = stats.ttest_ind(pair1, pair2)
        print(f"Question: {column} for group {pair[0]} (mean {round(pair1.mean(),3)}) vs group {pair[1]} (mean {round(pair2.mean().mean(),3)}).")
        print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
        print()
        print()


from utils import retrieveUserSurpriseDetails
df["Raw_Surprise"] = np.nan
df["Pred_Surprise"] = np.nan
df["Pred_Unfam"] = np.nan
df["Pred_Taste"] = np.nan

for index, row in df.iterrows():
    surp_details = retrieveUserSurpriseDetails(row["User_ID"],row["Recipe_ID"])
    df.at[index, "Raw_Surprise"] = surp_details["Raw Surprise"]
    df.at[index, "Pred_Surprise"] = surp_details["Predicted Surprise"]
    df.at[index, "Pred_Unfam"] = surp_details["Predicted Unfamiliarity"]
    df.at[index, "Pred_Taste"] = surp_details["Predicted Tastiness"]

qchef_stats = ["Raw_Surprise", "Pred_Surprise", "Pred_Unfam", "Pred_Taste"]
curiosity_qs = ["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_notcurious","curiosity_average"]

for qchef_stat in qchef_stats:
    surprise_bottom_third_thresh = df[qchef_stat].quantile(0.33)
    print(surprise_bottom_third_thresh)
    surprise_top_third_thresh = df[qchef_stat].quantile(0.67)
    print(surprise_top_third_thresh)

    df_bottom_third_surp = df[df[qchef_stat] < surprise_bottom_third_thresh]
    df_middle_third_surp = df[df[qchef_stat] >= surprise_bottom_third_thresh]
    df_middle_third_surp = df_middle_third_surp[df_middle_third_surp[qchef_stat] < surprise_top_third_thresh]
    df_top_third_surp = df[df[qchef_stat] >= surprise_top_third_thresh]

    thirds = [df_bottom_third_surp,df_middle_third_surp,df_top_third_surp]
    third_names = ["bottom", "mid", "top"]
    pairs = [(0,1), (0,2), (1,2)]

    for iteration_pair in pairs:
        iterationA = thirds[iteration_pair[0]]
        iterationB = thirds[iteration_pair[1]]
        for column in curiosity_qs:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if True:#  p_value < 0.055:
                print(f"Question: {column} for {third_names[iteration_pair[0]]} (mean {round(iterationA[column].mean(),3)}) vs {third_names[iteration_pair[1]]} (mean {round(iterationB[column].mean(),3)}), based on {qchef_stat}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()

    surprise_bottom_half_thresh = df[qchef_stat].quantile(0.5)

    df_bottom_half_surp = df[df[qchef_stat] < surprise_bottom_half_thresh]
    df_top_half_surp = df[df[qchef_stat] >= surprise_bottom_half_thresh]
    half_names = ["bottom",  "top"]
    for column in ["q1_wantknowtaste","q2_fascinating","q3_trymore","q4_learnmore","q5_notcurious","curiosity_average"]:
        t_stat, p_value = stats.ttest_ind(df_bottom_half_surp[column], df_top_half_surp[column])
        if True:#  p_value < 0.055:
            print(f"Question: {column} for bottom half (mean {round(iterationA[column].mean(),3)}) vs top half (mean {round(iterationB[column].mean(),3)}), based on {qchef_stat}.")
            print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
            print()
            print()

from itertools import product

for pair in list(product(qchef_stats, curiosity_qs)):
    corr = df[pair[0]].corr(df[pair[1]], method="spearman")
    r_squared = corr * corr
    print(f"Correlation between {pair[0]} and {pair[1]}: {round(corr, 3)}, R^2: {round(r_squared, 3)}")

# pairs = [(0,1), (0,2), (1,2)]
# pairs = [(0,2)]

# print("AVERAGES WITHIN GROUPS")
# for group_id,group in parsed_groups.items():
#     for iteration_pair in pairs:
#         iterationA = group[iteration_pair[0]]
#         iterationB = group[iteration_pair[1]]
#         for column in ["planning_average","freq_average","skill_average"]:
#             t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
#             print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} in group {group_id}")
#             print(f"t-statistic: {t_stat}")
#             print(f"P-value: {p_value}")

# combined_groups = [pd.concat([parsed_groups[0][i],parsed_groups[1][i],parsed_groups[2][i]],axis=0) for i in [0,1,2]]

# print("AVERAGES ACROSS GROUPS")
# for iteration_pair in pairs:
#     iterationA = combined_groups[iteration_pair[0]]
#     iterationB = combined_groups[iteration_pair[1]]
#     for column in ["planning_average","freq_average","skill_average"]:
#         t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
#         print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} across all groups")
#         print(f"t-statistic: {t_stat}")
#         print(f"P-value: {p_value}")

# print("INDIVIDUAL QUESTIONS WITHIN GROUPS")
# for group_id,group in parsed_groups.items():
#     for iteration_pair in pairs:
#         iterationA = group[iteration_pair[0]]
#         iterationB = group[iteration_pair[1]]
#         for column in planning_questions+freq_questions+skill_questions:
#             t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
#             print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} in group {group_id}")
#             print(f"t-statistic: {t_stat}")
#             print(f"P-value: {p_value}")


# print("INDIVIDUAL QUESTIONS ACROSS GROUPS")
# for iteration_pair in pairs:
#     iterationA = combined_groups[iteration_pair[0]]
#     iterationB = combined_groups[iteration_pair[1]]
#     for column in planning_questions+freq_questions+skill_questions:
#         t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
#         print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} across all groups")
#         print(f"t-statistic: {t_stat}")
#         print(f"P-value: {p_value}")

# Repeated Measures Anova 
import sys
sys.exit(0)

base_cols = ["User_ID","Experimental_Group","iteration_categories"]

allq_df = df[base_cols+['allq_mean']]
alcoholq_df = df[base_cols+['alcoholq_mean']]
dairyq_df = df[base_cols+['dairyq_mean']]
fruitq_df = df[base_cols+['fruitq_mean']]
carbq_df = df[base_cols+['carbq_mean']]
proteinq_df = df[base_cols+['proteinq_mean']]
otherq_df = df[base_cols+['otherq_mean']]
sweetsq_df = df[base_cols+['sweetsq_mean']]
vegq_df = df[base_cols+['vegq_mean']]



print(allq_df.head())
print("")
print("")
print("Allq ANOVA!")
allq_rm_anova_model = ols('allq_mean ~ C(Experimental_Group) * iteration_categories',data=allq_df).fit()
allq_rm_anova_results = sm.stats.anova_lm(allq_rm_anova_model, typ=2)
print(allq_rm_anova_results)
print("")
print("")

print("Alcoholq ANOVA!")
alcoholq_rm_anova_model = ols('alcoholq_mean ~ C(Experimental_Group) * iteration_categories',data=alcoholq_df).fit()
alcoholq_rm_anova_results = sm.stats.anova_lm(alcoholq_rm_anova_model, typ=2)
print(alcoholq_rm_anova_results)
print("")
print("")

print("Dairyq ANOVA!")
dairyq_rm_anova_model = ols('dairyq_mean ~ C(Experimental_Group) * iteration_categories',data=dairyq_df).fit()
dairyq_df_rm_anova_results = sm.stats.anova_lm(dairyq_rm_anova_model, typ=2)
print(dairyq_df_rm_anova_results)
print("")
print("")

print("Fruitq ANOVA!")
fruitq_rm_anova_model = ols('fruitq_mean ~ C(Experimental_Group) * iteration_categories',data=fruitq_df).fit()
fruitq_df_rm_anova_results = sm.stats.anova_lm(fruitq_rm_anova_model, typ=2)
print(fruitq_df_rm_anova_results)
print("")
print("")

print("Carbq ANOVA!")
carbq_rm_anova_model = ols('carbq_mean ~ C(Experimental_Group) * iteration_categories',data=carbq_df).fit()
carbq_df_rm_anova_results = sm.stats.anova_lm(carbq_rm_anova_model, typ=2)
print(carbq_df_rm_anova_results)
print("")
print("")

print("Proteinq ANOVA!")
proteinq_rm_anova_model = ols('proteinq_mean ~ C(Experimental_Group) * iteration_categories',data=proteinq_df).fit()
proteinq_df_rm_anova_results = sm.stats.anova_lm(proteinq_rm_anova_model, typ=2)
print(proteinq_df_rm_anova_results)
print("")
print("")

print("Otherq ANOVA!")
otherq_rm_anova_model = ols('otherq_mean ~ C(Experimental_Group) * iteration_categories',data=otherq_df).fit()
otherq_df_rm_anova_results = sm.stats.anova_lm(otherq_rm_anova_model, typ=2)
print(otherq_df_rm_anova_results)
print("")
print("")

print("Sweetsq ANOVA!")
sweetsq_rm_anova_model = ols('sweetsq_mean ~ C(Experimental_Group) * iteration_categories',data=sweetsq_df).fit()
sweetsq_df_rm_anova_results = sm.stats.anova_lm(sweetsq_rm_anova_model, typ=2)
print(sweetsq_df_rm_anova_results)
print("")
print("")

print("Vegq ANOVA!")
vegq_rm_anova_model = ols('vegq_mean ~ C(Experimental_Group) * iteration_categories',data=vegq_df).fit()
vegq_df_rm_anova_results = sm.stats.anova_lm(vegq_rm_anova_model, typ=2)
print(vegq_df_rm_anova_results)

# NEXT STEPS ARE TO aggregate the iterations into before (0), during (1-2), and after (3-4)
# and do a bunch of pairwise comparisons within that space.  Then break out specific groups, 
# and consider combining the surprise ones if needed.


#pairs = [("Before","During"), ("Before","After"), ("During","After")]
pairs = [(0,1), (0,2), (1,2)]

# All groups, between time
for iteration_pair in pairs:
    iterationA = df[df["iteration_categories"] == iteration_pair[0]]
    iterationB = df[df["iteration_categories"] == iteration_pair[1]]
    for column in ['allq_mean','alcoholq_mean','dairyq_mean','fruitq_mean','carbq_mean','proteinq_mean','otherq_mean','sweetsq_mean','vegq_mean']:
        t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
        if p_value < 0.055:
            print(f"Question: {column} for {iteration_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs {iteration_pair[1]} (mean {round(iterationB[column].mean(),3)}).")
            print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
            print()
            print()
        
# Individual experimental groups, between time
for experimental_group in [0,1,2]:
    for iteration_pair in pairs:
        iterationA = df[(df["iteration_categories"] == iteration_pair[0]) & (df["Experimental_Group"] == experimental_group)]
        iterationB = df[(df["iteration_categories"] == iteration_pair[1]) & (df["Experimental_Group"] == experimental_group)]
        for column in ['allq_mean','alcoholq_mean','dairyq_mean','fruitq_mean','carbq_mean','proteinq_mean','otherq_mean','sweetsq_mean','vegq_mean']:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if p_value < 0.105:
                print(f"Question: {column} for {iteration_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs {iteration_pair[1]}(mean {round(iterationB[column].mean(),3)}) for experimental group {experimental_group}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()

group_pairs = [(0,1),(0,2),(1,2)]

# Individual times, between experimental groups
for iteration in [0,1,2]:
    for group_pair in group_pairs:
        iterationA = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] == group_pair[0])]
        iterationB = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] == group_pair[1])]
        for column in ['allq_mean','alcoholq_mean','dairyq_mean','fruitq_mean','carbq_mean','proteinq_mean','otherq_mean','sweetsq_mean','vegq_mean']:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if p_value < 0.055:
                print(f"Question: {column} for group {group_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs group {group_pair[1]} (mean {round(iterationB[column].mean(),3)}) within iteration {iteration}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()


# Individual times, between experimental groups, with surprise and frontier combined
for iteration in [0,1,2]:
        iterationA = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] == 0)]
        iterationB = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] != 0)]
        for column in ['allq_mean','alcoholq_mean','dairyq_mean','fruitq_mean','carbq_mean','proteinq_mean','otherq_mean','sweetsq_mean','vegq_mean']:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if p_value < 0.055:
                print(f"Question: {column} for tasty (mean {round(iterationA[column].mean(),3)}) vs both (mean {round(iterationB[column].mean(),3)}) surprising groups within iteration {iteration}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()


qs = ["a1_beercider","a2_spirits","a3_wine","a4_otheralcohol","d1_milk","d2_butter","d3_cream","d4_cheese","d5_yoghurt","d6_eggs","d7_otherdairy","d8_dairysubs","f1_apples","f2_bananas","f3_citrus","f4_pears","f5_grapes","f6_mangos","f7_melons","f8_berries","f9_stonefruit","f10_otherfruit","f11_driedfruit","c1_flour","c2_corn","c3_oats","c4_rice","c5_pasta","c6_bread","c7_flatbread","c8_pizza","c9_bakedgoods","c10_othergrains","p1_whitefish","p2_oilyfish","p3_crustaceans","p4_squid","p5_molluscs","p6_otherseafood","p7_beef","p8_chicken","p9_pork","p10_lamb","p11_duck","p12_sausages","p13_curedmeat","p14_organs","p15_meatsubs","p16_othermeats","o1_teacoffee","o2_nuts","o3_seeds","o4_coconut","o5_soy","o6_oils","o7_proteinpowder","s1_sugar","s2_honey","s3_maple","s4_othersyrups","s5_jam","s6_chocolate","s7_icecream","s8_soda","s9_othersweets","s10_otherdesserts","v1_lettuce","v2_spinach","v3_rocket","v4_kale","v5_seaweed","v6_otherleafygreens","v7_cruciferous","v8_beans","v9_lentils","v10_peas","v11_garlic","v12_ginger","v13_chili","v14_mushrooms","v15_leek","v16_onions","v17_potatoes","v18_sweetpotatoes","v19_pumpkin","v20_othertubers","v21_tomatoes","v22_avocado","v23_asparagus","v24_capsicum","v25_zucchini","v26_eggplant","v27_fennel","v28_olives","v29_cucumbers","v30_pickledveg","v31_otherveg"]

# Individual questions, all groups, between times
for iteration_pair in pairs:
    iterationA = df[df["iteration_categories"] == iteration_pair[0]]
    iterationB = df[df["iteration_categories"] == iteration_pair[1]]
    for column in qs:
        t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
        if p_value < 0.055:
            print(f"Question: {column} for {iteration_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs {iteration_pair[1]} (mean {round(iterationB[column].mean(),3)}).")
            print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
            print()
            print()


# Individual questions, Individual times, between experimental groups
for iteration in [0,1,2]:
    for group_pair in group_pairs:
        iterationA = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] == group_pair[0])]
        iterationB = df[(df["iteration_categories"] == iteration) & (df["Experimental_Group"] == group_pair[1])]
        for column in qs:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if p_value < 0.055:
                print(f"Question: {column} for group {group_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs group {group_pair[1]} (mean {round(iterationB[column].mean(),3)}) within iteration {iteration}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()

import matplotlib.pyplot as plt

# Calculate the mean of each column
question_means = df[qs].mean()

# Sort the means in descending order
sorted_means = question_means.sort_values(ascending=False)

# Plot the sorted means
sorted_means.plot(kind='bar')

# Calculate the size of each third
third_size = len(sorted_means) // 3
remainder = len(sorted_means) % 3

# Add one to the top group until the remainder is exhausted
top_third_end = third_size + min(1, remainder)  # Add one if remainder exists
middle_third_end = top_third_end + third_size + (1 if remainder > 1 else 0)  # Add one if remainder is greater than one

# Break into thirds
top_third = sorted_means[:top_third_end].index.to_list()
middle_third = sorted_means[top_third_end:middle_third_end].index.to_list()
bottom_third = sorted_means[middle_third_end:].index.to_list()
df['top_third_mean'] = df[top_third].mean(axis=1)
df['middle_third_mean'] = df[middle_third].mean(axis=1)
df['bottom_third_mean'] = df[bottom_third].mean(axis=1)

top_half = sorted_means[:len(sorted_means) // 2].index.to_list()
bottom_half = sorted_means[len(sorted_means) // 2:].index.to_list()

df['top_half_mean'] = df[top_half].mean(axis=1)
df['bottom_half_mean'] = df[bottom_half].mean(axis=1)
# Comparing thirds, individual experimental groups, between time
for experimental_group in [0,1,2]:
    for iteration_pair in pairs:
        iterationA = df[(df["iteration_categories"] == iteration_pair[0]) & (df["Experimental_Group"] == experimental_group)]
        iterationB = df[(df["iteration_categories"] == iteration_pair[1]) & (df["Experimental_Group"] == experimental_group)]
        for column in ['top_third_mean','middle_third_mean','bottom_third_mean', 'top_half_mean', 'bottom_half_mean']:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            if p_value < 0.105:
                print(f"Question: {column} for {iteration_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs {iteration_pair[1]} (mean {round(iterationB[column].mean(),3)}) for experimental group {experimental_group}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()

# All groups, between time
for iteration_pair in pairs:
    iterationA = df[df["iteration_categories"] == iteration_pair[0]]
    iterationB = df[df["iteration_categories"] == iteration_pair[1]]
    for column in ['top_third_mean','middle_third_mean','bottom_third_mean', 'top_half_mean', 'bottom_half_mean']:
        t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
        if p_value < 0.105:
            print(f"Question: {column} for {iteration_pair[0]} (mean {round(iterationA[column].mean(),3)}) vs {iteration_pair[1]} (mean {round(iterationB[column].mean(),3)}).")
            print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
            print()
            print()

#NEW FOODS
# Can we track dietary novelty rather than diversity?
# What foods are people adding
# Comparing BETWEEN GROUPS, what foods were ADDED across iterations.  Before v During and Before v After for tasty v surprise.
     
# Individual experimental groups, between time
for group_pair in group_pairs:
    for iteration_pair in pairs:
        groupA_it1 = df[(df["iteration_categories"] == iteration_pair[0]) & (df["Experimental_Group"] == group_pair[0])]
        groupA_it2 = df[(df["iteration_categories"] == iteration_pair[1]) & (df["Experimental_Group"] == group_pair[0])]
        groupB_it1 = df[(df["iteration_categories"] == iteration_pair[0]) & (df["Experimental_Group"] == group_pair[1])]
        groupB_it2 = df[(df["iteration_categories"] == iteration_pair[1]) & (df["Experimental_Group"] == group_pair[1])]
        groupA_novelty_df = pd.DataFrame(columns=["User_ID"]+qs)
        groupA_novelty_df.set_index("User_ID",inplace=True)
        groupB_novelty_df = pd.DataFrame(columns=["User_ID"]+qs)
        groupB_novelty_df.set_index("User_ID",inplace=True)
        for uid in set(groupA_it1["User_ID"].unique()+groupA_it2["User_ID"].unique()): 
            user_rows_groupA_it1 = groupA_it1[groupA_it1["User_ID"]==uid]
            user_rows_groupA_it2 = groupA_it1[groupA_it2["User_ID"]==uid]           
            for q in qs:
                groupA_novelty_df.loc[uid,q] = user_rows_groupA_it1[q].any() & ~user_rows_groupA_it2[q].any()
            groupB_novelty_df[q] = groupB_it1[q] & ~groupB_it2[q]
        for column_name,column_set in zip(["all_qs","alcohol_qs","dairy_qs","fruit_qs","carb_qs","protein_qs","other_qs","sweets_qs","veg_qs"],[all_qs,alcohol_qs,dairy_qs,fruit_qs,carb_qs,protein_qs,other_qs,sweets_qs,veg_qs]):
            column = column_name+"_novelty"
            groupA_novelty_df[column] = groupA_novelty_df[column_set].mean(axis=1)
            groupB_novelty_df[column] = groupB_novelty_df[column_set].mean(axis=1)
            t_stat, p_value = stats.ttest_ind(groupA_novelty_df[column], groupB_novelty_df[column])
            if p_value < 0.105:
                print(f"Question: {column}  for {group_pair[0]} (mean {round(groupA_novelty_df[column].mean(),3)}) vs {group_pair[1]} (mean {round(groupB_novelty_df[column].mean(),3)}) between iterations {iteration_pair}.")
                print(f"t-statistic: {t_stat}, P-value: {round(p_value,3)}")
                print()
                print()
# # Set the title and labels
# plt.title('Mean Values for Each Question')
# plt.xlabel('Questions')
# plt.ylabel('Mean')

# # Show the plot
# plt.show()