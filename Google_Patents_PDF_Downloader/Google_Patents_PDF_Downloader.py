import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

class Google_Patents_PDF_Downloader:
    
    url = "https://patents.google.com"
    
    def __init__(self, verbose = False):
        self.verbose = verbose    
    
    def get_pdf(self, patent, output_path = "", driver_file = "chromedriver.exe", waiting_time = 6, remove_kind_codes = None):
       
        if remove_kind_codes is not None:
            for remove_kind_code in remove_kind_codes:
                patent = re.sub(remove_kind_code + "$", "", patent)
        
        ## get selenium started and open url
        driver = webdriver.Chrome(executable_path = driver_file)
        driver.get(self.url)
    
        element = driver.find_element_by_name('q')
        element.send_keys(patent)
        element.send_keys(Keys.RETURN)
        
        ## wait X secs
        time.sleep(waiting_time)
                
        ## get html code for page with expanded tree of recommendations
        raw_html = driver.page_source
        
        ## close browser
        driver.quit()
        
        ## parse html code from that webpage
        soup = BeautifulSoup(raw_html, 'html.parser')
           
        ## get specific part of html code
        soup2 = soup.find_all('a', class_ = 'style-scope patent-result')
        
        
        try:            
            ## identify PDF link in html source code
            pdf_link = soup2[0].attrs['href']
            
            ## download PDF
            myfile = requests.get(pdf_link)
            open(output_path + patent + '.pdf', 'wb').write(myfile.content)
            
            ## print statement
            print('Patent ' + patent + ' successfully downloaded')
            
        except:
            print("Error: Download link for patent " + patent + " not found!")
        
    def get_pdfs(self, patents = None, file = "", output_path = "", driver_file = "chromedriver.exe", waiting_time = 6, remove_kind_codes = None):        
                
        if file != "":
            df_patents = pd.read_csv(file)
            patents = list(df_patents['patent_number'])

        total = len(patents)        
        
        i = 1
        
        for patent in patents:
            
            self.get_pdf(patent = patent, output_path = output_path, driver_file = driver_file, 
                         waiting_time = waiting_time, remove_kind_codes = remove_kind_codes)

            remaining = total - i

            i += 1
            
            print(str(remaining) + " patent(s) remaining.")

            
            
            

        
        
        
        
        
        
        

        