from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Google_Patents_PDF_Downloader',
    version='0.1.0',
    description='Download Patents as PDF from Google Patents',
    long_description=readme,
    author='Lorenz Brachtendorf',
    author_email='lorenz.brachtendorf@gmx.de',
    url='https://github.com/lorenzbr/Google_Patents_PDF_Downloader',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

