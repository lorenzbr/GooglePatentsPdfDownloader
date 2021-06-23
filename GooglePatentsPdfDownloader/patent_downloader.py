import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

class patent_downloader:
    
    url = "https://patents.google.com"
    
    def __init__(self, verbose = False):
        self.verbose = verbose    
    
    def get_pdf(self, patent, output_path = "", driver_file = "chromedriver.exe", waiting_time = 6, remove_kind_codes = None):
        """ Download a patent document as a PDF        

        Parameters
        ----------
        patent : str
            A string containing a patent number (e.g., US4405829A1, EP0551921B1).
        output_path : str, optional
            An output path where documents are saved. The default is "".
        driver_file : str, optional
            Path and file name of the Chrome driver exe. The default is "chromedriver.exe".
        waiting_time : int, optional
            Waiting time in seconds for each request. The default is 6.
        remove_kind_codes : list, optional
            A list containing the patent kind codes which should be removed from patent numbers. The default is None.

        Returns
        -------
        None.

        """
       
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
        """ Download several patents as PDF documents        

        Parameters
        ----------
        patents : list, optional
            A list containing patent numbers (e.g., US4405829A1, EP0551921B1). The default is None.
        file : str, optional
            A string containing the path and file name. The needs to have one column with patent numbers. 
            The column name has to be patent_number. The default is "".
        output_path : str, optional
            An output path where documents are saved. The default is "".
        driver_file : str, optional
            Path and file name of the Chrome driver exe. The default is "chromedriver.exe".
        waiting_time : int, optional
            Waiting time in seconds for each request. The default is 6.
        remove_kind_codes : list, optional
            A list containing the patent kind codes which should be removed from patent numbers. The default is None.

        Returns
        -------
        None.
        
        Examples
        ----------
        See https://github.com/lorenzbr/GooglePatentsPdfDownloader#readme

        """
                
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
