## Download PDF documents of patents from Google patents
## URL: https://patents.google.com

## Examples

from GooglePatentsPdfDownloader.GooglePatentsPdfDownloader import GooglePatentsPdfDownloader
download = GooglePatentsPdfDownloader(verbose = True)

download.get_pdf(patent = "US4405829A1", output_path = "", driver_file = "chromedriver.exe")
download.get_pdfs(patents = ["US4405829A1", "EP0551921B1"], file = "", output_path = "", 
                  driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
download.get_pdfs(patents = None, file = "docs/data/patents.txt", output_path = "", 
                  driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
