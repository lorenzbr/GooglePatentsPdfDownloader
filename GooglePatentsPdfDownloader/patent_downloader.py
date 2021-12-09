from typing import List, Union, Optional
import requests
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class PatentDownloader:
    
    url = "https://patents.google.com"
    
    def __init__(self, verbose=False):
        self.verbose = verbose    
    
    def get_pdf(
            self,
            patent: str,
            output_path: str = "",
            driver_file: str = "chromedriver.exe",
            waiting_time: int = 6,
            remove_kind_codes: Optional[List[str]] = None):
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
        if remove_kind_codes:
            for remove_kind_code in remove_kind_codes:
                patent = re.sub(remove_kind_code + "$", "", patent)
        
        # get selenium started and open url
        driver = webdriver.Chrome(executable_path=driver_file)
        driver.get(self.url)
    
        # element = driver.find_element_by_name('q')
        element = driver.find_element('q')
        element.send_keys(patent)
        element.send_keys(Keys.RETURN)
        
        # wait X secs
        time.sleep(waiting_time)
                
        # get html code for page with expanded tree of recommendations
        raw_html = driver.page_source
        
        # close browser
        driver.quit()
        
        # parse html code from that webpage
        soup = BeautifulSoup(raw_html, 'html.parser')

        # get specific part of html code
        soup2 = soup.find_all('a', class_='style-scope patent-result')

        try:
            # identify PDF link in html source code
            pdf_link = soup2[0].attrs['href']
            
            # download PDF
            myfile = requests.get(pdf_link)
            open(f'{output_path}{patent}.pdf', 'wb').write(myfile.content)
            
            # print statement
            print(f'Patent {patent} successfully downloaded')
            
        except:
            print(f'Error: Download link for patent {patent} not found!')
        
    def get_pdfs(
            self,
            patents: Union[List[str], str],
            output_path: str = "",
            driver_file: str = "chromedriver.exe",
            waiting_time: int = 6,
            remove_kind_codes: Optional[List[str]] = None):
        """ Download several patents as PDF documents        

        Parameters
        ----------
        patents : list, str
            Ether a list containing patent numbers (e.g., US4405829A1, EP0551921B1),
            or a string containing the path and file name (CSV,TXT).
            The CSV needs a column named `patent_number`.
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
        if isinstance(patents, str):
            if patents.lower().endswith('csv'):
                df_patents = pd.read_csv(patents)
                patents = df_patents['patent_number'].to_list()
            elif patents.lower().endswith('txt'):
                with open(patents, 'r') as txt_file:
                    patents = txt_file.read().splitlines()
            else:
                raise NotImplementedError(f'Unsupported file type: {patents}')

        for i, patent in enumerate(patents):
            self.get_pdf(
                patent=patent,
                output_path=output_path,
                driver_file=driver_file,
                waiting_time=waiting_time,
                remove_kind_codes=remove_kind_codes
            )
            print(patents.size - i, " patent(s) remaining.")
