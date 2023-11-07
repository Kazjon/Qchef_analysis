import pandas as pd

filenames = [["data/FSQ_group0_iteration0.csv","data/FSQ_group0_iteration1.csv","data/FSQ_group0_iteration2.csv"],["data/FSQ_group1_iteration0.csv","data/FSQ_group1_iteration1.csv","data/FSQ_group1_iteration2.csv"],["data/FSQ_group2_iteration0.csv","data/FSQ_group2_iteration1.csv","data/FSQ_group2_iteration2.csv"]]

raw_groups = {}

for group in filenames:
    group_list = []
    for iteration in group:
        group_list.append(pd.read_csv(iteration))
    raw_groups[len(raw_groups.keys())] = group_list

parsed_groups = {}

frequency_lookup = {
    "Almost never": 0.,
    "Rarely": 1.,
    "Sometimes": 2.,
    "Often": 3.,
    "Almost always": 4.
}

times_lookup = {
    "<1 time per week": 0.,
    "1-2 times per week": 1.,
    "3-4 times per week": 2.,
    "5+ times per week": 3.
}

ability_lookup = {
    "I have no food preparation ability (eg. heating pre-prepared foods only)": 0.,
    "I have some food preparation ability (eg. make sandwiches, salads, or scrambled eggs),": 1.33,
    "I can use a combination of pre-prepared and basic ingredients to prepare homemade meals (eg, use pre-prepared rotisserie chicken in a home-made casserole),": 2.67,
    "I can prepare meals from basic ingredients (eg, make a chicken and vegetable stir-fry with rice)": 4.
}

#planning_questions = ["q1_bbd","q2_grocery","q3_buyvarveg","q4_confbudggroc","q5_confmealplan","q6_confselectveg","q7_confreadlabel","q8_planmealathome","q9_confadjustrecipe"]
#freq_questions = ["q10_timesownbrekkie","q11_timesownlunch","q12_timesowndinner"]
#skill_questions = ["q14_abilitytoprepare","q15_confknives","q16_confpeel","q17_confvegprep","q18_conflegume","q19_confprepbasic","q20_confrecipe","q21_confboil","q22_conffry","q23_confbake","q24_confspice","q25_confnew"]

freq_questions = ["q10_timesownbrekkie","q11_timesownlunch","q12_timesowndinner"]
planning_questions = ["q1_bbd","q2_grocery","q3_buyvarveg","q4_confbudggroc","q5_confmealplan","q6_confselectveg","q7_confreadlabel","q8_planmealathome","q9_confadjustrecipe"]
skill_questions = ["q13_oftenmealsbalanced","q14_abilitytoprepare","q15_confknives","q16_confpeel","q17_confvegprep","q18_conflegume","q19_confprepbasic","q20_confrecipe","q21_confboil","q22_conffry","q23_confbake","q24_confspice","q25_confnew"]

for groupnum,group in raw_groups.items():
    parsed_group_list = []
    for iteration in group:
        parsed_group = pd.DataFrame()
        parsed_group["User_ID"] = iteration["User_ID"]
        parsed_group["q1_bbd"] = iteration["q1_bbd"].replace(frequency_lookup)
        parsed_group["q2_grocery"] = iteration["q2_grocery"].replace(frequency_lookup)
        parsed_group["q3_buyvarveg"] = iteration["q3_buyvarveg"].replace(frequency_lookup)
        parsed_group["q4_confbudggroc"] = iteration["q4_confbudggroc"]-1.
        parsed_group["q5_confmealplan"] = iteration["q5_confmealplan"]-1.
        parsed_group["q6_confselectveg"] = iteration["q6_confselectveg"]-1.
        parsed_group["q7_confreadlabel"] = iteration["q7_confreadlabel"]-1.
        parsed_group["q8_planmealathome"] = iteration["q8_planmealathome"]-1.
        parsed_group["q9_confadjustrecipe"] = iteration["q9_confadjustrecipe"]-1.
        parsed_group["q10_timesownbrekkie"] = iteration["q10_timesownbrekkie"].replace(times_lookup)
        parsed_group["q11_timesownlunch"] = iteration["q11_timesownlunch"].replace(times_lookup)
        parsed_group["q12_timesowndinner"] = iteration["q12_timesowndinner"].replace(times_lookup)
        parsed_group["q13_oftenmealsbalanced"] = iteration["q13_oftenmealsbalanced"].replace(frequency_lookup)
        parsed_group["q14_abilitytoprepare"] = iteration["q14_abilitytoprepare"].replace(ability_lookup)
        parsed_group["q15_confknives"] = iteration["q15_confknives"]-1.
        parsed_group["q16_confpeel"] = iteration["q16_confpeel"]-1.
        parsed_group["q17_confvegprep"] = iteration["q17_confvegprep"]-1.
        parsed_group["q18_conflegume"] = iteration["q18_conflegume"]-1.
        parsed_group["q19_confprepbasic"] = iteration["q19_confprepbasic"]-1.
        parsed_group["q20_confrecipe"] = iteration["q20_confrecipe"]-1.
        parsed_group["q21_confboil"] = iteration["q21_confboil"]-1.
        parsed_group["q22_conffry"] = iteration["q22_conffry"]-1.
        parsed_group["q23_confbake"] = iteration["q23_confbake"]-1.
        parsed_group["q24_confspice"] = iteration["q24_confspice"]-1.
        parsed_group["q25_confnew"] = iteration["q25_confnew"]-1.
        parsed_group["planning_average"] = parsed_group[planning_questions].mean(axis=1)
        parsed_group["freq_average"] = parsed_group[freq_questions].mean(axis=1)
        parsed_group["skill_average"] = parsed_group[skill_questions].mean(axis=1)
        parsed_group_list.append(parsed_group)
    parsed_groups[len(parsed_groups.keys())] = parsed_group_list

from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

pairs = [(0,1), (0,2), (1,2)]
pairs = [(0,2)]

print("AVERAGES WITHIN GROUPS")
for group_id,group in parsed_groups.items():
    for iteration_pair in pairs:
        iterationA = group[iteration_pair[0]]
        iterationB = group[iteration_pair[1]]
        for column in ["planning_average","freq_average","skill_average"]:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} in group {group_id}")
            print(f"t-statistic: {t_stat}")
            print(f"P-value: {p_value}")

combined_groups = [pd.concat([parsed_groups[0][i],parsed_groups[1][i],parsed_groups[2][i]],axis=0) for i in [0,1,2]]

print("AVERAGES ACROSS GROUPS")
for iteration_pair in pairs:
    iterationA = combined_groups[iteration_pair[0]]
    iterationB = combined_groups[iteration_pair[1]]
    for column in ["planning_average","freq_average","skill_average"]:
        t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
        print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} across all groups")
        print(f"t-statistic: {t_stat}")
        print(f"P-value: {p_value}")

print("INDIVIDUAL QUESTIONS WITHIN GROUPS")
for group_id,group in parsed_groups.items():
    for iteration_pair in pairs:
        iterationA = group[iteration_pair[0]]
        iterationB = group[iteration_pair[1]]
        for column in planning_questions+freq_questions+skill_questions:
            t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
            print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} in group {group_id}")
            print(f"t-statistic: {t_stat}")
            print(f"P-value: {p_value}")


print("INDIVIDUAL QUESTIONS ACROSS GROUPS")
for iteration_pair in pairs:
    iterationA = combined_groups[iteration_pair[0]]
    iterationB = combined_groups[iteration_pair[1]]
    for column in planning_questions+freq_questions+skill_questions:
        t_stat, p_value = stats.ttest_ind(iterationA[column], iterationB[column])
        print(f"Question: {column} for iterations {iteration_pair[0]} and {iteration_pair[1]} across all groups")
        print(f"t-statistic: {t_stat}")
        print(f"P-value: {p_value}")

# Repeated Measures Anova 

planning_cols = ["User_ID","Group","Iteration","planning_score"]
planning_df = pd.DataFrame(columns=planning_cols)

skills_cols = ["User_ID","Group","Iteration","skill_score"]
skills_df = pd.DataFrame(columns=skills_cols)

freq_cols = ["User_ID","Group","Iteration","freq_score"]
freq_df = pd.DataFrame(columns=freq_cols)


confmealplan_cols = ["User_ID","Group","Iteration","q5_confmealplan"]
confmealplan_df = pd.DataFrame(columns=confmealplan_cols)


confadjustrecipe_cols = ["User_ID","Group","Iteration","q9_confadjustrecipe"]
confadjustrecipe_df = pd.DataFrame(columns=confadjustrecipe_cols)

confbalance_cols = ["User_ID","Group","Iteration","q13_oftenmealsbalanced"]
confbalance_df = pd.DataFrame(columns=confbalance_cols)

for group_id,group in parsed_groups.items():
    for iter_id,iteration in enumerate(group):
            group_column = pd.Series([group_id]*len(iteration),name="Group")
            iteration_column = pd.Series([iter_id]*len(iteration),name="Iteration")
            new_planning = pd.concat([iteration[["User_ID","planning_average"]],group_column,iteration_column],axis=1)
            new_planning = new_planning.rename(columns={"planning_average":"planning_score"})
            planning_df = pd.concat([planning_df,new_planning],ignore_index=True)
            new_skills = pd.concat([iteration[["User_ID","skill_average"]],group_column,iteration_column],axis=1)
            new_skills = new_skills.rename(columns={"skill_average":"skill_score"})
            skills_df = pd.concat([skills_df,new_skills],ignore_index=True)
            new_freqs = pd.concat([iteration[["User_ID","freq_average"]],group_column,iteration_column],axis=1)
            new_freqs = new_freqs.rename(columns={"freq_average":"freq_score"})
            freq_df = pd.concat([freq_df,new_freqs],ignore_index=True)
            new_q5s = pd.concat([iteration[["User_ID","q5_confmealplan"]],group_column,iteration_column],axis=1)
            confmealplan_df = pd.concat([confmealplan_df,new_q5s],ignore_index=True)
            new_q9s = pd.concat([iteration[["User_ID","q9_confadjustrecipe"]],group_column,iteration_column],axis=1)
            confadjustrecipe_df = pd.concat([confadjustrecipe_df,new_q9s],ignore_index=True)
            new_q13s = pd.concat([iteration[["User_ID","q13_oftenmealsbalanced"]],group_column,iteration_column],axis=1)
            confbalance_df = pd.concat([confbalance_df,new_q13s],ignore_index=True)

print(planning_df.head())
print("Planning ANOVA!")
planning_rm_anova_model = ols('planning_score ~ C(Group) * Iteration',data=planning_df).fit()
planning_rm_anova_results = sm.stats.anova_lm(planning_rm_anova_model, typ=2)
print(planning_rm_anova_results)


print("Skills ANOVA!")
skill_rm_anova_model = ols('skill_score ~ C(Group) * Iteration',data=skills_df).fit()
skill_rm_anova_results = sm.stats.anova_lm(skill_rm_anova_model, typ=2)
print(skill_rm_anova_results)


#print("Freq ANOVA!")
#freq_rm_anova_model = ols('freq_score ~ C(Group) * Iteration',data=freq_df).fit()
#freq_rm_anova_results = sm.stats.anova_lm(freq_rm_anova_model, typ=2)
#print(freq_rm_anova_results)


#print(confmealplan_df.head())
print("Q5 ANOVA!")
q5_rm_anova_model = ols('q5_confmealplan ~ C(Group) * Iteration',data=confmealplan_df).fit()
q5_rm_anova_results = sm.stats.anova_lm(q5_rm_anova_model, typ=2)
print(q5_rm_anova_results)


#print(confadjustrecipe_df.head())
print("Q9 ANOVA!")
q9_rm_anova_model = ols('q9_confadjustrecipe ~ C(Group) * Iteration',data=confadjustrecipe_df).fit()
q9_rm_anova_results = sm.stats.anova_lm(q9_rm_anova_model, typ=2)
print(q9_rm_anova_results)


#print(confbalance_df.head())
print("Q12 ANOVA!")
q13_rm_anova_model = ols('q13_oftenmealsbalanced ~ C(Group) * Iteration',data=confbalance_df).fit()
q13_rm_anova_results = sm.stats.anova_lm(q13_rm_anova_model, typ=2)
print(q13_rm_anova_results)