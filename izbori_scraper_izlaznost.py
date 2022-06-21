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
codes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,29,30,
         31,32,33,34,35,36,37,39,40,42,44,45,47,49,50,52,54,55,56,57,58,59,61,
         64,65,66,67,68,70,74,75,77,78,79,80,81,82,83,84,85,88,89,91,93,94,95,
         96,98,101,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,
         121,123,124,125,126,127,129,130,131,132,133,135,136,137,138,139,140,
         141,142,143,144,146,147,148,149,150,158,161,163,164,165,166,167,168,
         169,170,171,172,173,174,176,177,179,180,181,182,183,184,185,195]



#Pocetak tabele
data1 = np.array(['Mjesto','Broj birača','Broj listića'])



#Ovaj dio programa preuzima brojeve sa sajta izbori.ba
def scraper(URL, data):
    #kreiranje headless browsera i odlazak na pravi sajt
    options = Options()
    options.add_argument("--headless")    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.get(URL)
    
    #xPath svih relevantnih informacija sa sajta
    mjesto = '//*[@id="rightBar"]/div[1]/table/tbody/tr[1]/td'
    broj_biraca_xpath =  '//*[@id="rightBar"]/div[1]/table/tbody/tr[3]/td[1]'
    vazeci = '//*[@id="leftBar"]/div[6]/div/span'
    
    #Automatsko cekanje dok se brojevi ne ucitaju
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH,vazeci)))
    
    #Pronalazenje i sacuvanje teksta sa sajta
    element1 = driver.find_element(by=By.XPATH, value = mjesto)
    element2 = driver.find_element(by= By.XPATH, value = broj_biraca_xpath)
    element3 = driver.find_element(by= By.XPATH, value = vazeci)
    
    #formatiranje teksta sa sajta
    lokacija = element1.text
    broj_biraca = element2.text
    print(element2.text)
    broj_biraca2 = broj_biraca.replace(".","")
    broj_biraca1 = int(broj_biraca2)
    vazeci_listici = element3.text
    split = vazeci_listici.split(": ")
    listici = split[1]
    listici1 = int(listici.replace(".",""))
    driver.quit()
    
    #brojevi se dodaju u tabelu
    row = np.array([lokacija, broj_biraca1, listici1])
    data = np.vstack([data, row])
    return(data)

#Ponavljanje koda za svaku opstinu
for x in codes:
    url = 'https://www.izbori.ba/Rezultati_izbora/?resId=27&langId=1#/8/' + str(x) +'/null'
    data1 = scraper(url, data1)

#export tabele u csv file
pd.DataFrame(data1).to_csv("izlaznost.csv")







