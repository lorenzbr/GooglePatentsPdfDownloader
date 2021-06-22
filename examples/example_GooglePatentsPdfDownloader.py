## Download PDF documents of patents from Google Patents
## URL: https://patents.google.com

## Examples

from GooglePatentsPdfDownloader.patent_downloader import patent_downloader
patent_downloader = patent_downloader(verbose = True)

# Download a patent to the current working directory
patent_downloader.get_pdf(patent = "US4405829A1", output_path = "", driver_file = "chromedriver.exe")

# Download multiple patents from list of inputs to the current working directory
patent_downloader.get_pdfs(patents = ["US4405829A1", "EP0551921B1", "EP1304824B1"],
                           output_path = "", driver_file = "chromedriver.exe", 
                           remove_kind_codes = ["A1"])

# Download multiple patents from txt file to the current working directory
patent_downloader.get_pdfs(file = "docs/data/patents.txt", output_path = "",
                           driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
