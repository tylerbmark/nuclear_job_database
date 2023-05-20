from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
data_dict={
    'Southern Company':{
        'urls':['https://southerncompany-nuclear.jobs/#3'],
        'jobs_tag':'li',
        'jobs_class':'direct_joblisting',
        'title_tag':'span',
        'title_class':'resultHeader',
        'location_tag':'span',
        'location_class':'hiringPlace',
        'url_tag':'a',
        'url_class':'href',
        'xPath':'/html/body/div[2]/div/div[3]/ul[2]/li[1]'
    },
    'Westinghouse':{
        'urls':['https://careers.westinghousenuclear.com/search/?q=&q2=&alertId=&locationsearch=&geolocation=&searchby=location&d=10&lat=&lon=&title=nuclear&location=&date='],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'title_tag':'a',
        'title_class':'jobTitle-link',
        'location_tag':'span',
        'location_class':'jobLocation',
        'url_tag':'a',
        'url_class':'href',
        'xPath':'/html/body/div[2]/div[2]/div/div/div[4]/table/tbody/tr[1]'
    },
    'Duke Energy':{
    'urls':['https://dukeenergy.wd1.myworkdayjobs.com/search?q=nuclear'],
    'jobs_tag':'li',    
    'jobs_class':'css-1q2dra3',
    'title_tag':'div',
    'title_class':'css-b3pn3b',
    'location_tag':'dd',
    'location_class':'css-129m7dg',
    'url_tag':'a',
    'url_class':'href',
    'xPath':'/html/body/div/div/div/div[3]/div/div/div[2]/section/ul/li[1]'
    },
    'LANL':{ #not working
        'urls':['https://jobsp1.lanl.gov/OA_HTML/OA.jsp?page=/oracle/apps/irc/candidateSelfService/webui/VisAdJobSchPG&_ri=821&SeededSearchFlag=Y&DaysSincePosting=1001&_ti=129777394&retainAM=Y&addBreadCrumb=S&oapc=2&oas=epFLitlLOHrWYedY_zgo_Q..'],
        'jobs_tag':'tr',
        'jobs_class':'xha',
        'title_tag':'td',
        'title_class':'x1t x50 xmz',
        'location_tag':'',
        'location_class':'',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[3]/form/span[2]/div[3]/div/div[1]/div/div[4]/div[1]/div[2]/table[2]/tbody/tr[4]/td/table/tbody/tr/td/div/div/span[1]/div/div/div[1]/div[3]/table[1]/tbody/tr[1]', 
    },
    'BWXT':{
        'urls':['https://careers.bwxt.com/go/Recent-Grad-and-Student-Jobs/3930400/'],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'span',
        'location_class':'jobLocation',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[2]/div[2]/div/div/div[6]/div[2]/table/tbody/tr[1]', 
    },
    'NuScale':{# Doesnt work
        'urls':['https://www.nuscalepower.com/en/about/careers/job-openings'],
        'jobs_tag':'div',
        'jobs_class':'jv-careersite',
        'title_tag':'td',
        'title_class':'jv-job-list-name',
        'location_tag':'td',
        'location_class':'jv-job-list-location',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[1]/div[2]/div[4]', 
    },
    'TerraPower':{
        'urls':['https://www.terrapower.com/contact-us/careers/'],
        'jobs_tag':'div',
        'jobs_class':'vc_col-sm-6 wpb_column column_container vc_column_container col child_column no-extra-padding inherit_tablet inherit_phone ',
        'title_tag':'div',
        'title_class':'rbox-opening-li',
        'location_tag':'div',
        'location_class':'rbox-job-shortdesc',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[1]/div/div[3]/div[1]/div/div/div[6]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[3]/div[2]', 
    }

}

# soup=BeautifulSoup(html,'html.parser')
# job_listings=soup.find_all('li',class_='css-1q2dra3')
# for job_listing in job_listings:
#     title = job_listing.find('div',class_='css-b3pn3b').text.strip()
#     location = job_listing.find('dd', class_='css-129m7dg').text.strip()
#     link = job_listing.find('a')['href']
#     # Print the extracted information
#     print(f'Title: {title}\nLocation: {location}\nLink: {link}\n')

for employer in list(data_dict.keys())[6:]:
    for url in data_dict[employer]['urls']:
        print(employer)
        driver=webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        
        wait=WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH, data_dict[employer]['xPath'])))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html=driver.page_source
        driver.quit()
        # Send a GET request to the URL and parse the HTML using BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        # Find all of the job listings on the page
        print(soup)
        job_listings = soup.find_all(data_dict[employer]['jobs_tag'], class_=data_dict[employer]['jobs_class'])
        
        # # Iterate over each job listing and extract the title, location, and link
        print(job_listings)
        for job_listing in job_listings:
            print(job_listing)
            title = job_listing.find(data_dict[employer]['title_tag'],class_=data_dict[employer]['title_class']).text.strip()
            location = job_listing.find(data_dict[employer]['location_tag'], class_=data_dict[employer]['location_class']).text.strip()
            link = job_listing.find(data_dict[employer]['url_tag'])[data_dict[employer]['url_class']]
            
            # try:
            #     title = job_listing.find(data_dict[employer]['title_tag'],class_=data_dict[employer]['title_class']).text.strip()
            # except: 
            #     title=''
            # try:
            #     location = job_listing.find(data_dict[employer]['location_tag'], class_=data_dict[employer]['location_class']).text.strip()
            # except:
            #     location=''
            # try:
            #     link = job_listing.find(data_dict[employer]['url_tag'])[data_dict[employer]['url_class']]
            # except:
            #     link=''
            # print(i)
            # Print the extracted information
            print(f'Title: {title}\nLocation: {location}\nLink: {link}\n')

# print(job_listings)