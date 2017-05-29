import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gsheet io",
    version = ".1",
    author = "Ben Holmes",
    author_email = "ben@aeronaut.net",
    description = ("tools for reading spreadsheets on google into flatfiles & datbase"),
    license = "MIT",
    keywords = "aeronaut",
    url = "http://github.com/bh0085/gsheet-io",
    install_requires=['sqlalchemy','dateparser','gspread','oauth2client'],
    packages=[''],
    long_description=read('README.md')
)
