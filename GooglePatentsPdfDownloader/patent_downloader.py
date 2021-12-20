from typing import List, Union, Optional
import os
import requests
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class PatentDownloader:
    
    url = "https://patents.google.com"
    
    def __init__(self, chrome_driver: str = 'chromedriver.exe', brave: bool = False, verbose: bool = False):
        """

        Parameters
        ----------
        chrome_driver : str
            Path and file name of the Chrome driver exe. Default is "chromedriver.exe".
        brave : bool, optional
            Change Chrome application for Brave by passing 'brave'. Default is None.
        """
        self.verbose = verbose  # TODO: unused attribute?
        self.driver_file = chrome_driver
        self.option = None
        if brave:
            brave_path = brave_application_path()
            self.option = webdriver.ChromeOptions()
            self.option.binary_location = brave_path
            self.option.add_argument("--incognito")

    def download(self,
                 patent: Union[str, List[str]],
                 output_path: str = "./",
                 waiting_time: int = 6,
                 remove_kind_codes: Optional[List[str]] = None) -> None:
        """Download patent document(s) as PDF

        Parameters
        ----------
        patent : str, list[str]
            Patent(s) to download.
            Ether a string containing a patent number (e.g., US4405829A1, EP0551921B1),
            or a list containing patent numbers,
            or a string containing the path and file name (CSV,TXT). The CSV needs a column named `patent_number`.
        output_path : str, optional
            An output path where documents are saved. Default is "./".
        waiting_time : int, optional
            Waiting time in seconds for each request. The default is 6.
        remove_kind_codes : list, optional
            A list containing the patent kind codes which should be removed from patent numbers. Default is None.

        Returns
        -------
        None.

        Examples
        ----------
        See https://github.com/lorenzbr/GooglePatentsPdfDownloader#readme
        """
        try:
            valid_path = os.path.isfile(patent)
        except TypeError:
            valid_path = False

        if valid_path or isinstance(patent, list):
            self.get_pdfs(
                patents=patent,
                output_path=output_path,
                waiting_time=waiting_time,
                remove_kind_codes=remove_kind_codes
            )
        else:
            self.get_pdf(
                patent=patent,
                output_path=output_path,
                waiting_time=waiting_time,
                remove_kind_codes=remove_kind_codes
            )

    def get_pdf(self, patent: str, output_path: str = "./", waiting_time: int = 6,
                remove_kind_codes: Optional[List[str]] = None) -> None:

        if remove_kind_codes:
            for remove_kind_code in remove_kind_codes:
                patent = re.sub(remove_kind_code + "$", "", patent)
        
        # get selenium started and open url
        if self.option:
            driver = webdriver.Chrome(executable_path=self.driver_file, options=self.option)
        else:
            driver = webdriver.Chrome(executable_path=self.driver_file)
        driver.get(self.url)
    
        element = driver.find_element_by_name('q')
        element.send_keys(patent)
        element.send_keys(Keys.RETURN)
        time.sleep(waiting_time)  # wait X secs
        raw_html = driver.page_source  # get html code for page with expanded tree of recommendations
        driver.quit()  # close driver
        
        # parse html code from that webpage
        soup = BeautifulSoup(raw_html, 'html.parser')
        pdf_link = self.get_pdf_link(soup, patent)

        if pdf_link:
            path_prefix = os.path.abspath(output_path)
            validate_directory(path_prefix)
            patent_file = requests.get(pdf_link)
            with open(os.path.join(path_prefix, f'{patent}.pdf'), 'wb') as pdf_file:
                pdf_file.write(patent_file.content)
            print(f'>>> Patent {patent} successfully downloaded <<<')  # print statement
        else:
            pass

    def get_pdfs(self, patents: Union[List[str], str], output_path: str = "./", waiting_time: int = 6,
                 remove_kind_codes: Optional[List[str]] = None) -> None:
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
            print(len(patents) - i, "patent(s) remaining.")
            self.get_pdf(
                patent=patent,
                output_path=output_path,
                waiting_time=waiting_time,
                remove_kind_codes=remove_kind_codes
            )

    @staticmethod
    def get_pdf_link(soup: BeautifulSoup, patent: str):
        pdfs: List[str] = [link['href'] for link in soup.find_all('a', href=True)
                           if link['href'].lower().endswith('pdf')]
        for pdf in pdfs:
            if patent.lower() in pdf.lower():  # TODO: ignore/remove kind code?
                return pdf  # return first matching pdf link
            else:
                continue
        print(f'Error: Download link for patent {patent} not found!')
        return None


def brave_application_path() -> str:
    win_paths = [
        r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe',
    ]
    # TODO: add paths?
    for win_path in win_paths:
        if os.path.isfile(win_path):
            return win_path
        else:
            pass
    raise FileNotFoundError


def validate_directory(directory: str) -> None:
    if os.path.isdir(directory):
        return None
    os.mkdir(directory)