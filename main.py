import time
import os
import sys
import pandas as pd
import pygsheets
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def launch_driver(URL,unique_rpps):
    """Lancement du driver à l'adresse souhaité"""

    def nb_element_result_page():
        """rechercher le nombre de résulta par page et les stocker dans une list"""
        time_out_find_result=60
        # div_results = WebDriverWait(browser, time_out_find_result).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'contenant_resultats_scroll')))
        # list_elem_result = WebDriverWait(div_results, time_out).until(
        #         EC.presence_of_all_elements_located((By.CLASS_NAME,'contenant_resultat')))
        list_elem_result=[]
        try:
            list_elem_result = WebDriverWait(browser, time_out_find_result).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.contenant_resultat a')))
        except TimeoutException:
            print("pas de RPSS " + str(rpps_gsheet))
            pass
        list_nom_prenom=[]
        if list_elem_result != []:
            for el in list_elem_result:
                list_nom_prenom.append(el.accessible_name)

        
        # list_elem_profession = WebDriverWait(browser, time_out_find_result).until(
        #         EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.contenant_resultat .profession')))
        # list_elem_tel = WebDriverWait(browser, time_out_find_result).until(
        #         EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.contenant_resultat .tel')))
        return list_nom_prenom

    def click_on_each_result_page(list_nom_prenom,browser):
        '''click sur chacun des éléments trouvé par par page'''
        # nb_row = len(datasheet.index)
        time_out=1000
        # while nb_row !=list_elem_result:
        for idx,name_el in enumerate(list_nom_prenom):
            if name_el == '':
                continue
            nom_prenom=''
            list_elem_result = WebDriverWait(browser, time_out).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.contenant_resultat a')))
            if idx ==0:
                list_elem_result[idx].send_keys(Keys.RETURN)
            else:
                list_elem_result[idx].send_keys(Keys.RETURN)
                while nom_prenom != name_el:
                    try:
                        el_nom_prenom = WebDriverWait(browser, time_out).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'.popin_resultats_details_h .nom_prenom')))
                        nom_prenom=el_nom_prenom.text
                    except:
                        print("erreur")
                        pass
            try:
                time_out_email = 15
                email=''
                email_el = WebDriverWait(browser, time_out_email).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.labelEmail a')))
                email=email_el.text
            except TimeoutException:
                print("pas d'email")
                pass

            try:
                time_out_email = 5
                email_mmsSante=''
                email_mmsSante = WebDriverWait(browser, time_out_email).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.labelMssante')))
                email_mmsSante=email_mmsSante.text
            except TimeoutException:
                print("pas d'email mmSante")
                pass
                
            rpps = WebDriverWait(browser, time_out).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.rpps span')))
            nom_prenom = WebDriverWait(browser, time_out).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.popin_resultats_details_h .nom_prenom')))
            profession = WebDriverWait(browser, time_out).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.popin_resultats_details_h .profession')))
            # datasheet.append({'RPPS':rpps.text.split(' ')[-1]}, ignore_index=True)

            datasheet.loc[datasheet['national_number']==rpps_gsheet,'RPPS']=rpps.text.split(' ')[-1]
            # datasheet["RPPS"][datasheet['national_number']==rpps_gsheet]=rpps.text.split(' ')[-1]
            # datasheet.loc[idx_df,'RPPS']=rpps.text.split(' ')[-1]
            if email !='':
                datasheet.loc[datasheet['national_number']==rpps_gsheet,'Mail']=email
                # datasheet["Mail"][datasheet['national_number']==rpps_gsheet]=email
                # datasheet.loc[idx_df,'Mail']=email
            if email_mmsSante !='':
                datasheet.loc[datasheet['national_number']==rpps_gsheet,'Mail Santé']=email_mmsSante
                # datasheet["Mail Santé"][datasheet['national_number']==rpps_gsheet]=email_mmsSante
                # datasheet.loc[idx_df,'Mail Santé']=email_mmsSante
            datasheet.loc[datasheet['national_number']==rpps_gsheet,'Nom et Prénom']=nom_prenom.text
            datasheet.loc[datasheet['national_number']==rpps_gsheet,'Profession']=profession.text

            # datasheet["Nom et Prénom"][datasheet['national_number']==rpps_gsheet]=nom_prenom.text
            # datasheet["Profession"][datasheet['national_number']==rpps_gsheet]=profession.text
            # datasheet.loc[idx_df,'Profession']=profession.text
            # datasheet.loc[idx_df,'Nom et Prénom']=nom_prenom.text
        wait_true= True
        return
            
    def get_tel_people(browser):
        """Récupération des infos dans la liste contenant_resultat """
        list_elem_result = WebDriverWait(browser, time_out).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.contenant_resultat')))
        for idx,el in enumerate(list_elem_result):
            try:
                time_out_tel = 5
                tel=""
                tel = WebDriverWait(el, time_out_tel).until(
                EC.presence_of_element_located((By.CLASS_NAME,'tel')))
            except TimeoutException:
                print("pas de tel donné")
                pass
            if tel !="":
                datasheet.loc[datasheet['national_number']==rpps_gsheet,'Tél']=tel.text
                # datasheet.loc[idx_df,'Tél']=tel.text
            # nom_prenom= el.accessible_name

    # def  next_page(browser) :
    #     """Clique sur la page suivante"""
    #     current_page=  WebDriverWait(browser, time_out).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR,'.taglib-page-iterator .on a'))).accessible_name
    #     nb_page_available=  WebDriverWait(browser, time_out).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR,'.nombre span')))

    #     if len(nb_page_available)==1:
    #         pass
    #     else :
    #         next_page=int(current_page) + 1
    #         for idx,el in enumerate(nb_page_available):
    #             if int(el.accessible_name) == next_page:
    #                 page_to_click = WebDriverWait(el, time_out).until(
    #             EC.presence_of_element_located((By.TAG_NAME,'a')))
    #                 page_to_click.send_keys(Keys.RETURN)
           


    if os.path.exists("/Applications/Internet/Google Chrome.app/Contents/MacOS/Google Chrome"):
        path_google_chrome="/Applications/Internet/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:
        path_google_chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options = Options()
    options.binary_location = path_google_chrome
    options.add_experimental_option("detach", True)
    rel_path="/Applications/chromedriver"
    PATH = os.path.abspath(rel_path)
    browser = webdriver.Chrome(options=options,executable_path=PATH)
    
    
    # RPPS_START= "101*"

    for idx_df,rpps_gsheet in enumerate(unique_rpps):
        if (type(rpps_gsheet) is not int):
            # datasheet.loc[idx_df,'Annuaire Santé Check']='CHECK'
            datasheet.loc[datasheet['national_number']==rpps_gsheet,'Annuaire Santé Check']="CHECK"
            # datasheet["Annuaire Santé Check"][datasheet['national_number']==rpps_gsheet]="CHECK"
            continue
        if(len(str(rpps_gsheet)) != 11):
            datasheet.loc[datasheet['national_number']==rpps_gsheet,'Annuaire Santé Check']="CHECK"
            # datasheet.loc[idx_df,'Annuaire Santé Check']='CHECK'
            # datasheet["Annuaire Santé Check"][datasheet['national_number']==rpps_gsheet]="CHECK"
            continue
        # TEST 
        # if idx_df < 10:
        #     continue
         # TEST 
        print(rpps_gsheet)
        print(idx_df)
        browser.get(URL)
        element_xpath = WebDriverWait(browser,time_out).until(EC.presence_of_element_located((By.XPATH,"//input[@name='_rechercheportlet_INSTANCE_X1yv3htFTpVn_identifiant']")))
        
        browser.execute_script("arguments[0].value = ''", element_xpath)
        element_xpath.send_keys(rpps_gsheet)
        div_valider = WebDriverWait(browser, time_out).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ligne_reinitialiser')))
        btn_valider = WebDriverWait(div_valider, time_out).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
        btn_valider[0].send_keys(Keys.RETURN)

        list_nom_prenom = nb_element_result_page()
        if list_nom_prenom != []:
            click_on_each_result_page(list_nom_prenom,browser)
            get_tel_people(browser)
        
        datasheet.loc[datasheet['national_number']==rpps_gsheet,'Annuaire Santé Check']="CHECK"
        # datasheet.loc[idx_df,'Annuaire Santé Check']='CHECK'
        # datasheet["Annuaire Santé Check"][datasheet['national_number']==rpps_gsheet]="CHECK"


    # next_page(browser)

    WAIT=True

def get_data_sheet(wk,wk_to_update):
    """Get column RPPS Google sheet"""

    datasheet_to_update=wk_to_update.get_as_df()
    # col_numbers = [ord(letter[0]) - 96 for letter in rpps_col]
    # pd_col_rpps=wk.get_col(col_numbers[0])
    datasheet_all=wk.get_as_df()

    unique_rpps=list(set(datasheet_all['national_number']))

    # index_rpps=[ datasheet_all.index[datasheet_all['national_number']==el].tolist() for el in unique_rpps ]
    row_first_empty_check = datasheet_to_update[datasheet_to_update['Annuaire Santé Check']==""].index.values.astype(int)[0]+2

    return_data=datasheet_all.loc[:,cols_info_people].copy()
    return return_data,row_first_empty_check,unique_rpps

def copy_data_to_sheet(row_first_empty_check,start_column):
    """Senf data to google sheet"""
    df_to_paste = datasheet.iloc[:,1:].copy()
    col_number = [ord(letter[0]) - 96 for letter in start_column]

    wk_to_update.set_dataframe(df_to_paste,(int(row_first_empty_check),col_number[0]),copy_head=False)


if __name__ == "__main__":
    gc = pygsheets.authorize(client_secret='/Users/acapai/Documents/Git/Espace-test/Scrapping-With-Python/ManageGoogleSheetPython/code_secret_client_173621592213-0llal3ntmv316usvtboglpb52leq6jcu.apps.googleusercontent.com.json')
    sh = gc.open_by_key('1-q8eTH-BJPJHbuwR-DDbKz8T5wnr_lXqVl46Cq-yJ4M')

    dict_config_typeform = {"col_name_rpps":"national_number","wk_to_update":2,"wk":3,"rpps_col":["c"], "start_column":["t"]}
    dict_config_vidal = {"col_name_rpps":"national_number","wk_to_update":0,"wk":4,"rpps_col":["c"], "start_column":["t"]}

    dict_to_check = dict_config_typeform.copy()

    rpps_name=dict_to_check["col_name_rpps"]
    wk_to_update=sh[dict_to_check["wk_to_update"]]
    wk = sh[dict_to_check["wk"]]
    rpps_col= dict_to_check["rpps_col"]
    start_column=dict_to_check["start_column"]
    row_start=[1]
    if (wk.title == "RPPS to search - VIDAL" or wk.title == "RPPS to search - Typeform") :
        URL = "https://annuaire.sante.fr/web/site-pro/recherche/rechercheDetaillee"
        
        cols_info_people = [rpps_name,"Nom et Prénom","Profession","Mail","Mail Santé", "Tél", "RPPS","Annuaire Santé Check"]
        time_out = 30
        # datasheet = pd.DataFrame(columns=cols_info_people)
        datasheet,row_first_empty_check,unique_rpps=get_data_sheet(wk,wk_to_update)
        launch_driver(URL,unique_rpps)

        # START_ROW=2
        copy_data_to_sheet(row_first_empty_check,start_column)

    WAIT=True