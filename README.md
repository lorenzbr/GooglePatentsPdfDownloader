# Google_Patents_PDF_Downloader

Download patents as PDF documents from [Google Patents](https://patents.google.com)


## Installation

You can install the development version from [GitHub](https://github.com/) with:

``` python
pip install git+https://github.com/lorenzbr/Google_Patents_PDF_Downloader.git
```

Please make sure you have [Google Chrome](https://www.google.com/chrome/) and the corresponding chromedriver.exe (see [here](https://chromedriver.chromium.org/downloads)) installed to access the website using Selenium.


## Examples

```python
from Google_Patents_PDF_Downloader import Google_Patents_PDF_Downloader
download = Google_Patents_PDF_Downloader(verbose = True)

download.get_pdf(patent = "US4405829A1", output_path = "", driver_file = "chromedriver.exe")
download.get_pdfs(patents = ["US4405829A1", "EP0551921B1"], file = None, output_path = "", driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
download.get_pdfs(patents = None, file = "docs/data/patents.txt", output_path = "", driver_file = "chromedriver.exe", remove_kind_codes = ["A1"])
```

## License

This repository is licensed under the MIT license.

See [here](https://github.com/lorenzbr/Google_Patents_PDF_Downloader/blob/master/LICENSE) for further information.