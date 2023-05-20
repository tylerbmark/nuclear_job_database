# nuclear_job_database
This project is designed to compile a database of all nuclear related jobs for undergraduates to use when applying for jobs or internships. The project uses BeautifulSoup to parse HTML from a job postings and will add the information to a public spreadsheet using Google Sheets. This project is meant to make the field more accessible and competitive by giving undergraduates access to the same resources in the form of an easy-to-navigate database. 

# Link to current database:
[Google Drive link](https://docs.google.com/spreadsheets/d/1ceaF-h6sflCJAfwCDBvrAmjnN3MBVQef/edit?usp=share_link&ouid=114343353415857691307&rtpof=true&sd=true)

# Instructions:
## Setting up environment and packages
To create a python environment:\
``python -m venv /path/to/new/virtual/environment``

To activate the package:\
`` ./path/to/new/virtual/environment/activate ``

Install the following packages:\
``pip install bs4 selenium pandas numpy requests openpyxl``
## Chrome Drivers
To use Selenium, Chrome Drivers must be installed which is straightforward
1. Download and install a ChromeDriver and move the file over to the project folder
https://chromedriver.chromium.org/downloads
2. Rename this line in ``main.py`` to point to your driver file location
``driver=webdriver.Chrome('chromedriver.exe') ``
3. (Not as important) Install the Drive for desktop application to update the database to Google Drive for the finished product. I'll likely have a raspberry pi automatically do this.  https://www.google.com/drive/download/
# Current Considered Employers on Database
* Southern Company
* Westinghouse
* Duke Energy
* BWXT
* TerraPower
* Urenco
* General Atomics
* Entergy
* Orano
* Cameco Corporation
* GE Hitachi Nuclear Energy
* Enercon
* First Energy
* NextEra Energy
* Constellation
* Engie

# Future Work
* Reading multiple pages on the websites
* Continuing to add new companies
    * Nuscale
    * LANL 
    * EnergySolutions
    * Kairos
    * NEI (not nuclear)
    * Areva (Orano? )
    * Unistar Nuclear Energy
* Adding National Labs and Universities
# Special Thanks to

