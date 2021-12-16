import argparse
from .patent_downloader import PatentDownloader


parser = argparse.ArgumentParser(
    prog='GooglePatentsPdfDownloader',
    description='Download patent document(s) as PDF from GooglePatents'
)
parser.add_argument(
    'patent', nargs='+', help='Patent number(s) to be downloaded')
parser.add_argument(
    '--driver', help='Path and file name of the Chrome driver exe', default='chromedriver.exe')
parser.add_argument(
    '--brave', help='Switch application from Google Chrome to Brave.', action='store_true')
parser.add_argument(
    '--output', help='An output path where documents are saved', default='./pdf')
parser.add_argument(
    '--time', type=int, help='Waiting time in seconds for each request.', default=6)
parser.add_argument(
    '--rm-kind', nargs='+', type=str,
    help='A list containing the patent kind codes which should be removed from patent numbers'
)

args = parser.parse_args()
kwargs = dict(
    patent=args.patent,
    output_path=args.output,
    waiting_time=args.time,
    remove_kind_codes=args.rm_kind
)

if args.brave:
    pat_dl = PatentDownloader(chrome_driver=args.driver, brave=args.brave)
else:
    pat_dl = PatentDownloader(chrome_driver=args.driver)

pat_dl.download(**kwargs)
