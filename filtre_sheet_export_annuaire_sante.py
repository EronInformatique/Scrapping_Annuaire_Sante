import pandas as pd
from fuzzywuzzy import process,fuzz
import os
import itertools
# Give the location of the file
# loc = ("/Users/acapai/Documents/Git/Espace-test/Scrapping-With-Python/Scrapping_annuaire-sante/FILTRER_ExtractionMonoTable_CAT18_ToutePopulation_202203230921.xlsx")

dir=os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv('/Users/acapai/Documents/Git/Espace-test/Scrapping-With-Python/Scrapping_annuaire-sante/FILTRER_ExtractionMonoTable_CAT18_ToutePopulation_202203230921.csv',sep=';',on_bad_lines='skip', encoding='utf-8')

# To open Workbook
# wb = xlrd.open_workbook(loc)
# pd.read_pickle("/Users/acapai/Documents/Git/Espace-test/Scrapping-With-Python/Scrapping_annuaire-sante/data_sup_ratios_set_token_one_41")
df_imported_without_nan = pd.read_pickle(os.path.join(dir,"data_with_score_fuzzy_without_nan"))
if len(df_imported_without_nan)==1:
    values_raison_sociale = df["Raison sociale site"].unique()
    cols_info_people = ["Raison Sociale","Hopital","CHU","CH","HOP","CHRU","Hopital CHU CH HOP CHRU HU"]
    datasheet = pd.DataFrame(columns=cols_info_people)
    datasheet.loc[:,'Raison Sociale']=values_raison_sociale
    datasheet.iloc[:,1:] = datasheet.iloc[:,1:] .fillna(0)
    print (df)
    nan_list=datasheet[datasheet['Raison Sociale'].isnull()].index.tolist()
    for index, row in datasheet.iterrows():
        element_to_compare=datasheet.loc[index,"Raison Sociale"]
        if index not in nan_list :
            ratios = process.extract(element_to_compare,cols_info_people[1:],limit=len(cols_info_people[1:]),scorer=fuzz.ratio)
            ratios_partial = process.extract(element_to_compare,cols_info_people[1:],limit=len(cols_info_people[1:]),scorer=fuzz.partial_ratio)
            ratios_partial_token = process.extract(element_to_compare,cols_info_people[1:],limit=len(cols_info_people[1:]),scorer=fuzz.partial_token_set_ratio)
            ratios_token = process.extract(element_to_compare,cols_info_people[1:],limit=len(cols_info_people[1:]),scorer=fuzz.token_set_ratio)

            ratios_one = process.extractOne(element_to_compare,cols_info_people[1:],scorer=fuzz.ratio)
            ratios_partial_one = process.extractOne(element_to_compare,cols_info_people[1:],scorer=fuzz.partial_ratio)
            ratios_partial_token_one = process.extractOne(element_to_compare,cols_info_people[1:],scorer=fuzz.partial_token_set_ratio)
            ratios_set_token_one = process.extractOne(element_to_compare,cols_info_people[1:],scorer=fuzz.token_set_ratio)
            print("ratios_set_one",element_to_compare ,ratios_set_token_one)
            print("ratios_partial_token_one",element_to_compare ,ratios_partial_token_one)
            print("ratios_partial_one",element_to_compare ,ratios_partial_one)
            print("ratios_one",element_to_compare ,ratios_one)
            print("\n \n \n \n \n")
            # ratios_one_w = process.extractWithoutOrder(element_to_compare,cols_info_people[1:],scorer=fuzz.ratio)
            # ratios_partial_one_w= process.extractWithoutOrder(element_to_compare,cols_info_people[1:],scorer=fuzz.partial_ratio)
            # ratios_partial_token_one_w = process.extractWithoutOrder(element_to_compare,cols_info_people[1:],scorer=fuzz.partial_token_set_ratio)
            # ratios_token_one_w = process.extractWithoutOrder(element_to_compare,cols_info_people[1:],scorer=fuzz.token_set_ratio)

            datasheet.loc[index,ratios_partial_one[0]]=ratios_one[1]

    # data_with_score_fuzzy=datasheet.copy()
    # data_with_score_fuzzy.to_pickle(os.path.join(dir,"data_with_score_fuzzy"))

    data_with_score_fuzzy_without_nan=datasheet.copy()
    data_with_score_fuzzy_without_nan.to_pickle(os.path.join(dir,"data_with_score_fuzzy_without_nan"))

fuzzy_method="ratios_set_token_one"
value_to_filter=41
list_index_to_remove2D=[]
for col in df_imported_without_nan.columns[1:]:
    df_mask_toremove=df_imported_without_nan.loc[:,col]>=value_to_filter
    filtered_df = df_imported_without_nan.loc[df_mask_toremove,"Raison Sociale"].tolist()
    list_index_to_remove2D.append(filtered_df[:])

list_index_to_remove_one = list(itertools.chain(*list_index_to_remove2D))


data_score_fuzzy_sup=df_imported_without_nan[df_imported_without_nan["Raison Sociale"].isin(list_index_to_remove_one)]
data_clean=df_imported_without_nan[~df_imported_without_nan["Raison Sociale"].isin(list_index_to_remove_one)]

data_clean.to_pickle(os.path.join(dir,"data_clean"))
data_score_fuzzy_sup.to_pickle(os.path.join(dir,f"data_sup_{fuzzy_method}_{value_to_filter}"))

df_global_score_fuzzy_inf = df[~df["Raison sociale site"].isin(list_index_to_remove_one)]
df_global_score_fuzzy_inf.to_pickle(os.path.join(dir,f"data_clean_full_{fuzzy_method}_{value_to_filter}"))
df_global_score_fuzzy_inf.to_excel(os.path.join(dir,f"data_clean_full_{fuzzy_method}_{value_to_filter}_.xlsx"))  

wait_here=True
