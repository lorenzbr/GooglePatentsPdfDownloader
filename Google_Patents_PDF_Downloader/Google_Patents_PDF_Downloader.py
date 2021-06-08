# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:37:51 2019


Patent PDF Downloader for google patents

To Do: 
    - remove kind codes in patent number as google often does not find the patent when the kind code is included
    - produce table with error messages when google does not find patent number and jump to next patent

@author: bral
"""






## import python modules
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time



## set wd
os.chdir('Z:\Daten\SEPSIM')

## specify which driver to use
driver_name = "chromedriver.exe"
#driver_name_old = "chromedriver_old.exe"

## input path
input_path = 'IEEE/declarations/'

## output path
output_path = 'IEEE/declarations/patent_pdfs/'


## read csv
df_patents = pd.read_csv(input_path+'ieee_declarations_unique_patent_numbers.csv')

##
patents = list(df_patents['patent_number'])


## set url where do download pdfs
url = 'https://patents.google.com'

i = 1

patents_nokindcode = [patent.replace("A1","") for patent in patents]
patents_nokindcode = [patent.replace("B1","") for patent in patents_nokindcode]

## for loop over all patents
for patent in patents_nokindcode[691:744]:
    
    ## get selenium started and open url
    driver = webdriver.Chrome(executable_path="Z:\\Eigene Dateien\\Promotion\\04 Software\\Geckodriver\\"+driver_name)
    driver.get(url)

    ##
    element = driver.find_element_by_name('q')
    element.send_keys(patent)
    element.send_keys(Keys.RETURN)
    
    ## wait X secs
    time.sleep(6)
    
    ## current url
#    driver.current_url
    
    ## get html code for page with expanded tree of recommendations
    raw_html = driver.page_source
    
    ## close browser
    driver.quit()
    
    ## parse html code from that webpage
    soup = BeautifulSoup(raw_html,'html.parser')
       
    ## get specific part of html code
    soup2 = soup.find_all('a',class_ = 'style-scope patent-result')
    
    ## identify PDF link in html source code
    pdf_link = soup2[0].attrs['href']
    
    ## download pdf
    myfile = requests.get(pdf_link)
    open(output_path+patent+'.pdf', 'wb').write(myfile.content)
    
    ## print statement
    print('No.' + str(i) + ':    Patent ' + patent + ' successfully downloaded')
    
    ## increase by 1
    i += 1
    
    
    
    
    