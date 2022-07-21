import requests 
from selenium import webdriver
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd


#Ovo je link za lokalne izbore 2020 i brojevi ispod toga su kodovi svih opstina
#koje su izasle na izbore taj dan. Ukoliko se ovaj program koristi za druge
#izbore mozda ce biti potrebno promjeniti kodove, ili implementirati da 
#automatski mijenja
codes = [6,7,8,9,10,11,12,13,14,16,18,20,21,23,24,26,28,29,
         31,33,34,35,38,40,45,54,56,58,61,
         64,66,68,70,74,81,83,88,89,101,103,104,105,108,
         121,123,132,138,139,140,
         142,144,146,147,158,161,163,164,166,168,
         169,170,177,179,180,182,184,185]



#Pocetak tabele
# data1 = np.array(['Mjesto','Broj birača','Broj listića'])



#Ovaj dio programa preuzima brojeve sa sajta izbori.ba
def scraper(URL):
    #kreiranje headless browsera i odlazak na pravi sajt
    options = Options()
    options.add_argument("--headless")    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.get(URL)
    
    #xPath svih relevantnih informacija sa sajta
    tabela = '//*[@id="rightBar"]/div[4]/table/tbody'
    opstina = '//*[@id="rightBar"]/div[2]/table/tbody/tr[1]/td'
    #Automatsko cekanje dok se brojevi ne ucitaju
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH,tabela)))
    
    #Pronalazenje i sacuvanje teksta sa sajta
    element1 = driver.find_element(by=By.XPATH, value = tabela)
    element2 = driver.find_element(by=By.XPATH, value = opstina)

    #formatiranje teksta sa sajta
    tabela1 = element1.text
    opstina1 = element2.text
    rezultat = np.array([tabela1,opstina1])
    driver.quit()
    #brojevi se dodaju u tabelu
    # row = np.array([lokacija, broj_biraca1, listici1])
    
    return(rezultat)

data = ['Sifra', 'Kandidat','Broj glasova','%']


def rezultati(URL, table):
    data1 = scraper(URL)
    data2 = data1[1]
    data1 = data1[0]
    data1 = data1.split("\n")
    length = len(data1) - 1
    for x in data1[1:]:
        x = x.replace("," ,"")
        x = x.replace("." ,"")
        strings = []
        for word in x.split():
            if not word.isdigit():
                strings.append(word)
        numbers = []
        for word in x.split():
            if word.isdigit():
                numbers.append(int(word))
        stranka = ' '.join(strings)
        numbers.insert(1,stranka)
        table = np.vstack([table, numbers])
    table2 = np.repeat(data2,length)
    table2 = np.insert(table2, 0, "opstina")
    table = np.c_[table2, table]
    return table


#Ponavljanje koda za svaku opstinu
URL = 'http://www.izbori.ba/rezultati_izbora?resId=25&langId=1#/1/2/132/0/0'


#TODO: srediti
tabela = rezultati(URL, data)
procenti = tabela[1:,4]
procenti1 = procenti.astype(np.float)
procenti1 = procenti1/100
simbol = np.array("%")
procenti1 = np.r_[simbol, procenti1]
tabela = tabela[:,:4]
tabela = np.c_[tabela, procenti1]

#export tabele u csv file
# pd.DataFrame(tabela).to_csv("nacelnik.csv")