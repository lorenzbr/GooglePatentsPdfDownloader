# Google Patents PDF Downloader

Download patents as PDF documents from [Google Patents](https://patents.google.com)


## Installation

You can install the development version from [GitHub](https://github.com/) with:

``` python
pip install git+https://github.com/lorenzbr/GooglePatentsPdfDownloader.git
```

Please make sure you have [Google Chrome](https://www.google.com/chrome/) and the corresponding chromedriver.exe (see [here](https://chromedriver.chromium.org/downloads)) installed to access the website using Selenium.


## Run GooglePatentsPdfDownloader

```
python -m GooglePatentsPdfDownloader
  patent      Patent number(s) to be downloaded

optional arguments:
  --driver    Path and file name of the Chrome driver exe
  --app       Switch application from Google Chrome to Brave. Valid value: "brave"
  --output    An output path where documents are saved
  --time      Waiting time in seconds for each request.
  --rm-kind   A list containing the patent kind codes which should be removed from patent numbers
```

## Examples
Download a single patent to the current working directory (not found w/ kind code)
```bash
python -m GooglePatentsPdfDownloader US4405829A1 --rm_kind A1
python -m GooglePatentsPdfDownloader EP0551921B1
```
Download multiple patents using a list of inputs to ./pdf directory
```bash
python -m GooglePatentsPdfDownloader US4405829 EP0551921B1 --output "./pdf"
```
With Brave browser download multiple patents using a txt file to the current working director
```bash
python -m GooglePatentsPdfDownloader docs/data/patents.txt --app brave
```

## Examples (modular)
```python
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
    patent="docs/data/patents.txt", 
    output_path="",
    remove_kind_codes=["A1"]
)
```

## License

This repository is licensed under the MIT license.

See [here](https://github.com/lorenzbr/GooglePatentsPdfDownloader/blob/master/LICENSE) for further information.