from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
from lxml import etree

data_dict={
    'Southern Company':{
        'urls':['https://southerncompany-nuclear.jobs/#3'],
        'jobs_tag':'li',
        'jobs_class':'direct_joblisting',
        'jobs_id':'',
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
        'jobs_id':'',
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
        'jobs_id':'',
        'title_tag':'div',
        'title_class':'css-b3pn3b',
        'location_tag':'dd',
        'location_class':'css-129m7dg',
        'url_tag':'a',
        'url_class':'href',
        'xPath':'/html/body/div/div/div/div[3]/div/div/div[2]/section/ul/li[1]'
    },
    'BWXT':{
        'urls':['https://careers.bwxt.com/go/Recent-Grad-and-Student-Jobs/3930400/'],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'jobs_id':'',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'span',
        'location_class':'jobLocation',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[2]/div[2]/div/div/div[6]/div[2]/table/tbody/tr[1]', 
    },
    'TerraPower':{
        'urls':['https://www.terrapower.com/contact-us/careers/'],
        'jobs_tag':'div',
        'jobs_class':'rbox-opening-li',
        'jobs_id':'',
        'title_tag':'a',
        'title_class':'rbox-opening-li-title',
        'location_tag':'div',
        'location_class':'rbox-job-shortdesc',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[1]', 
    },
    'Urenco':{
        'urls':['https://www.urenco.com/careers/vacancies/u-usa'],
        'jobs_tag':'div',
        'jobs_class':'reports uk-text-center tsunami-bg',
        'jobs_id':'',
        'title_tag':'h3',
        'title_class':'uk-margin-bottom',
        'location_tag':'',
        'location_class':'',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[3]/div[9]/div', 
    },
    'General Atomics':{# Works but needs to read multiple pages
        'urls':['https://www.ga-careers.com/search-jobs/nuclear?orgIds=499&kt=1&ac=376'],
        'jobs_tag':'li',
        'jobs_class':'',
        'jobs_id':'',
        'title_tag':'h2',
        'title_class':'',
        'location_tag':'span',
        'location_class':'job-location',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div/main/div[1]/div/div[2]/section', 
    },
    'Entergy':{
        'urls':['https://jobs.entergy.com/go/Nuclear/4350700/'],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'jobs_id':'',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'span',
        'location_class':'jobLocation',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[2]/div[2]/div/div/div[5]/div[2]/table/tbody/tr[1]', 
    },

    'Orano':{
        'urls':['https://www.orano.group/jobs/en/our-offers?Page=1&Keywords=nuclear','https://www.orano.group/jobs/en/our-offers?Page=2&Keywords=nuclear'],
        'jobs_tag':'li',
        'jobs_class':'result-item',
        'jobs_id':'',
        'title_tag':'h3',
        'title_class':'result-title',
        'location_tag':'div',
        'location_class':'mr-3 d-flex',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div/div/div[3]/main/div[2]/div[2]/div/ul',   
    },
    'Cameco':{ # Need to add multiple pages
        'urls':['https://career17.sapsf.com/career?company=Cameco&career%5fns=job%5flisting%5fsummary&navBarLevel=JOB%5fSEARCH&_s.crb=WXl0EKE4OuePFGQ%2f4phs%2boAy6K1hlTLbgup0a8Vj%2bTc%3d'],
        'jobs_tag':'tr',
        'jobs_class':'jobResultItem',
        'jobs_id':'',
        'title_tag':'a',
        'title_class':'jobTitle',
        'location_tag':'span', #Need to fix location, only gives job id
        'location_class':'jobContentEM',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '//*[@id="36:"]/table/tbody/tr[6]', 
    },
    'GE Hitachi NE':{ # need to specify united states, and multiple pages
        'urls':['https://jobs.gecareers.com/gepel'],
        'jobs_tag':'li',
        'jobs_class':'jobs-list-item',
        'jobs_id':'',
        'title_tag':'a',
        'title_class':'au-target',
        'location_tag':'span',
        'location_class':'job-location',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[2]/div[2]/div/div/div/div[2]/section[2]/div/div/div/div[1]/div[2]/div[2]/ul/li[8]', 
    },
    'Enercon':{
        'urls':['https://phe.tbe.taleo.net/phe03/ats/careers/v2/searchResults?org=ENERCON2&cws=37'],
        'jobs_tag':'div',
        'jobs_class':'oracletaleocwsv2-accordion oracletaleocwsv2-accordion-expandable clearfix',
        'jobs_id':'',
        'title_tag':'h4',
        'title_class':'oracletaleocwsv2-head-title',
        'location_tag':'div', #fix location
        'location_class':'',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[2]/section[5]/div/div/div[2]/div/div[1]', 
    },
    'FirstEnergy':{
        'urls':['https://careers.firstenergycorp.com/go/Co-OpInternship-Opportunities/3340500/','https://careers.firstenergycorp.com/go/Engineering-Opportunities/3340400/'],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'jobs_id':'',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'td', 
        'location_class':'colLocation hidden-phone',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html', 
    },
    'NextEra':{
        'urls':['https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/',
                'https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/25/?q=&sortColumn=referencedate&sortDirection=desc',
                'https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/50/?q=&sortColumn=referencedate&sortDirection=desc'],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'jobs_id':'',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'td', 
        'location_class':'colLocation hidden-phone',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html',   
    },
    'Constellation Energy':{
        'urls':[F'https://jobs.constellationenergy.com/jobs/search?location=&page={i}&q=nuclear#' for i in range(17)],
        'jobs_tag':'div',
        'jobs_class':'jobs-section__item',
        'jobs_id':'',
        'title_tag':'div',
        'title_class':'col-lg-6 col-sm-12',
        'location_tag':'div', 
        'location_class':'col-lg-4 col-sm-12',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html',   
    },
    'Engie':{
        'urls':['https://jobs.engie.com/search/?createNewAlert=false&q=nuclear&locationsearch=']+
            [F'https://jobs.engie.com/search/?q=nuclear&startrow={i}' for i in range(25,150,25)],
        'jobs_tag':'tr',
        'jobs_class':'data-row',
        'jobs_id':'',
        'title_tag':'span',
        'title_class':'jobTitle hidden-phone',
        'location_tag':'span', 
        'location_class':'jobLocation',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html',      
    },
    'Framatone':{
        'urls':['https://www.framatome.com/en/jobseekers/job-offers/'],
        
    },
    'Idaho NL':{ # Can't seem to filter 
        'urls':['https://inl.taleo.net/careersection/inl_external/jobsearch.ftl?lang=en&portal=8110010144#'],
        'jobs_tag':'tr',
        'jobs_class':'even',
        'jobs_id':'',
        'title_tag':'div',
        'title_class':'absolute',
        'location_tag':'', 
        'location_class':'',
        'url_tag':'a',
        'url_class':'href',
        'xPath': '/html/body/div[3]/div/div[3]/div[5]/div[3]/div[3]/div[3]/div[2]/table/tbody/tr[1]',      
    },
    'Oak Ridge National Lab':{
        'urls':['https://jobs.ornl.gov/search/?q=nuclear&searchby=location&d=10',]+
        [F'https://jobs.ornl.gov/search/?q=nuclear&searchby=location&d=10&startrow={i}' for i in range(25,100,25)],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr[1]/td[1]/span/a',  
    },
    'Lawrence Livermore NL':{# Doesn't work
        'urls':['https://www.llnl.gov/join-our-team/careers/find-your-job/156da5cf-5933-4153-874f-cfd786065564/nuclear'],
        'title_xpath':'//*[@id="onelab-content"]/div/div/div/div/div/div/div/a[1]',
        # 'location_xpath':'//*[@id="onelab-content"]/div/div[3]/div[2]/div[1]/div/div/small[2]/i',
        'location_xpath':'',
        'location_place':'Livermore, CA',
        'url_xpath':'//*[@id="onelab-content"]/div/div/div/div/div/div/div/a[1]',  
    },
    'Sandia NL':{
        'urls':[
            'https://sandia.jobs/jobs/?q=nuclear',
            'https://sandia.jobs/jobs/?q=nuclear&page=2',
            'https://sandia.jobs/jobs/?q=nuclear&page=3'],
        'title_xpath':'//*[@id="jobs"]/li/div/a/h2',
        # 'title_xpath':'/html/body/div[1]/div/div/div[1]/div/div/div/div/main/div/ul[1]/li/div/a/h2',
        'location_xpath':'//*[@id="jobs"]/li/div/a/p[1]',
        'location_place':'',
        'url_xpath':'//*[@id="jobs"]/li/div/a',
    },
    'Helion Fusion':{
        'urls':['https://www.helionenergy.com/careers/'],
        'title_xpath':'//*[@id="job-list-table"]/li/div/p',
        'location_xpath':'',
        'location_place':'Everett, WA',
        'url_xpath':'//*[@id="job-list-table"]/li/div/div/a',
    },
    'Brookhaven NL':{
        'urls':['https://jobs.bnl.gov/search-jobs/nuclear?orgIds=3437&kt=1'],
        'title_xpath':'//*[@id="search-results-list"]/ul/li/a/h2',
        'location_xpath':'//*[@id="search-results-list"]/ul/li/a/span',
        'location_place':'',
        'url_xpath':'//*[@id="search-results-list"]/ul/li/a',
    },
    # 'EnergySolutions':{# Doesn't work
    #     'urls':['https://energy-solution.com/careers/'],
    #     'jobs_tag':'tr',
    #     'jobs_class':'reqitem ReqRowClick ReqRowClick',
    #     'jobs_id':'',
    #     'title_tag':'td',
    #     'title_class':'posTitle reqitem ReqRowClick',
    #     'location_tag':'td',
    #     'location_class':'cities reqitem ReqRowClick',
    #     'url_tag':'a',
    #     'url_class':'href',
    #     'xPath':'/html/body/div/div/div/article/div/div/div/div[3]/div[1]/div[2]/div/div/iframe'
    #     # 'xPath':'//*[@class="reqitem ReqRowClick ReqRowClick"]'
    # }
    # 'Kairos':{ # Doesn't work
    #     'urls':['https://kairospower.com/careers/'],
    #     'title_xpath':'/html/body/div/div/div/section[1]/div/a',
    #     'location_xpath':'//*[@id="search-results-list"]/ul/li/a/span',
    #     'location_place':'',
    #     'url_xpath':'//*[@id="search-results-list"]/ul/li/a',   
    # }

    # 'NuScale':{# Doesnt work
    #     'urls':['https://www.nuscalepower.com/en/about/careers/job-openings'],
    #     'title_xpath':'/html/body/div/div/div/article/div/table[3]/tbody/tr[1]/td[1]/a',
    #     'location_xpath':'//*[@id="search-results-list"]/ul/li/a/span',
    #     'location_place':'',
    #     'url_xpath':'//*[@id="search-results-list"]/ul/li/a',       
    #     },
    # 'LANL':{ #not working
    #     'urls':['https://jobsp1.lanl.gov/OA_HTML/OA.jsp?page=/oracle/apps/irc/candidateSelfService/webui/VisAdJobSchPG&_ri=821&SeededSearchFlag=Y&DaysSincePosting=1001&_ti=129777394&retainAM=Y&addBreadCrumb=S&oapc=2&oas=epFLitlLOHrWYedY_zgo_Q..'],
    #     'jobs_tag':'tr',
    #     'jobs_class':'xha',
    #     'title_tag':'td',
    #     'title_class':'x1t x50 xmz',
    #     'location_tag':'',
    #     'location_class':'',
    #     'url_tag':'a',
    #     'url_class':'href',
    #     'xPath': '/html/body/div[3]/form/span[2]/div[3]/div/div[1]/div/div[4]/div[1]/div[2]/table[2]/tbody/tr[4]/td/table/tbody/tr/td/div/div/span[1]/div/div/div[1]/div[3]/table[1]/tbody/tr[1]', 
    # },
}

def init_files():
    df_test=pd.DataFrame({
        'Title':[''],
        'Locations':[''],
        'Url':['']
    })
    key_list=list(data_dict.keys())
    for i in range(len(key_list)):
        # df_test[key_list[i]]=['']
        try:
            with pd.ExcelWriter('data.xlsx',engine='openpyxl',mode='a',if_sheet_exists='replace') as writer:
                df_test.to_excel(writer,sheet_name=key_list[i],index=False)
        except:
            with pd.ExcelWriter('data.xlsx',engine='openpyxl',mode='w') as writer:
                df_test.to_excel(writer,sheet_name=key_list[i],index=False)
            
init_files()
for employer in list(data_dict.keys())[-1:]:
    url_ind=0
    for url in data_dict[employer]['urls']:
        print(employer)
        url_ind+=1
        driver=webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        
        # html = driver.execute_script("return document.documentElement.innerHTML")
        html=driver.page_source
        
        driver.quit()

        # Send a GET request to the URL and parse the HTML using BeautifulSoup
        # f=open('test.txt','r')
        # html=f.read()
        # f.close()
        soup = BeautifulSoup(html, 'html.parser')
        soup.find_all(data_dict)
        dom = etree.HTML(str(soup))

        # print(job_listings[0].get('href'))
        
        df_old=pd.read_excel('data.xlsx',sheet_name=employer)
        df_job_title=list(df_old['Title'])
        df_job_location=list(df_old['Locations'])
        df_job_url=list(df_old['Url'])
        # print(len(job_listings))
        df_job_title=df_job_title+[i.text for i in dom.xpath(data_dict[employer]['title_xpath'])]
        if data_dict[employer]['location_xpath']=='':
            df_job_location=df_job_location+[data_dict[employer]['location_place']]*len(dom.xpath(data_dict[employer]['title_xpath']))
        else:
            df_job_location=df_job_location+[i.text for i in dom.xpath(data_dict[employer]['location_xpath'])]
        df_job_url=df_job_url+[i.get('href') for i in dom.xpath(data_dict[employer]['url_xpath'])]
        print('Titles:')
        for i in df_job_title:
            print(i)
        print('Locations:')
        for i in df_job_location:
            print(i)
        print('urls')
        for i in df_job_url:
            print(i)
        
        print(len(df_job_title),len(df_job_location),len(df_job_url))
        # print('title: ',df_job_title,'\nlocation: ',df_job_location,'\nurl: ',df_job_url)
        df=pd.DataFrame({
            'Title':df_job_title,
            'Locations':df_job_location,
            'Url':df_job_url
        })
        with pd.ExcelWriter("data.xlsx",mode='a',if_sheet_exists='replace') as writer:
            df.to_excel(writer,sheet_name=employer)


# print(job_listings)