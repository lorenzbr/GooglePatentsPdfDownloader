## Download PDF documents of patents from Google Patents
## URL: https://patents.google.com

from GooglePatentsPdfDownloader import PatentDownloader
patent_downloader = PatentDownloader(chrome_driver='chromedriver.exe', app='brave')

# Download a single patent to the current working directory (not found w/ kind code)
patent_downloader.download(patent="US4405829A1", remove_kind_codes=['A1'])
patent_downloader.download(patent="EP0551921B1")


# Download multiple patents using a list of inputs to the current working directory
patent_downloader.download(
    patent=["US4405829A1", "EP0551921B1", "EP1304824B1"],
    output_path="./pdf_files",
    remove_kind_codes=["A1"]
)

# Download multiple patents using a txt file to the current working directory
patent_downloader.download(
    patent="../docs/data/patents.txt",
    output_path="",
    remove_kind_codes=["A1"]
)