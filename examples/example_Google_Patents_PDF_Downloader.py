## Download PDF documents of patents from Google patents
## URL: https://patents.google.com

## Examples

from Google_Patents_PDF_Downloader import Google_Patents_PDF_Downloader
download = Google_Patents_PDF_Downloader(verbose = True)

download.get_pdf(patent = "US4405829A1", output_path = "", driver_file = "chromedriver.exe")
download.get_pdfs(patents = ["US4405829A1", "EP0551921B1"], file = None, output_path = "", driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
download.get_pdfs(patents = None, file = "docs/data/patents.txt", output_path = "", driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
