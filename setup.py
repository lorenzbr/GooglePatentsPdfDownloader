from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = 'GooglePatentsPdfDownloader',
    version = '0.1.0',
    description = 'Download patents as PDF documents from Google Patents',
    long_description = readme,
    author = 'Lorenz Brachtendorf',
    author_email = 'lorenz.brachtendorf@gmx.de',
    url = 'https://github.com/lorenzbr/GooglePatentsPdfDownloader',
    license = license,
    packages = find_packages(exclude = ('tests', 'docs')),
    install_requires = ['requests', 'bs4', 'pandas', 'selenium', 'numpy'],
    include_package_data = True
)

