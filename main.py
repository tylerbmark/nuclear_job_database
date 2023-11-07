from lxml import etree
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os

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
    #     'jobs_tag':'div',
    #     'jobs_class':'opening',
    #     'jobs_id':'',
    #     'title_tag':'div',
    #     'title_class':'opening',
    #     'location_tag':'span',
    #     'location_class':'location',
    #     'url_tag':'a',
    #     'url_class':'href',
    #     'xPath': '/html/body/div/div/iframe',         
    # }

    # 'NuScale':{# Doesnt work
    #     'urls':['https://www.nuscalepower.com/en/about/careers/job-openings'],
    #     'jobs_tag':'table',
    #     'jobs_class':'jv-job-list',
    #     'jobs_id':'',
    #     'title_tag':'td',
    #     'title_class':'jv-job-list-name',
    #     'location_tag':'td',
    #     'location_class':'jv-job-list-location',
    #     'url_tag':'a',
    #     'url_class':'href',
    #     'xPath': '/html/body/div/div/div',
    # },
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
async def get_html(url):
        browser = await launch(headless=True,executablePath='/usr/bin/chromium-browser')
        page = await browser.newPage()
        await page.goto(url)
        html=await page.content()
        await browser.close()
        return html

def init_files():
    df_test=pd.DataFrame({
        'Title':[''],
        'Locations':[''],
        'Url':['']
    })
    key_list=list(data_dict.keys())
    for i in range(len(key_list)):
        # df_test[key_list[i]]=['']
        with pd.ExcelWriter('data.xlsx',engine='openpyxl',mode='a',if_sheet_exists='replace') as writer:
            df_test.to_excel(writer,sheet_name=key_list[i],index=False)
init_files()
for employer in list(data_dict.keys())[::-1]:
    url_ind=0
    for url in data_dict[employer]['urls']:
        print(employer)
        url_ind+=1
        html=asyncio.get_event_loop().run_until_complete(get_html(url))
        # Send a GET request to the URL and parse the HTML using BeautifulSoup
        # f=open('test.txt','w')
        # f.write(html)
        # f.close()
        
        soup = BeautifulSoup(html, 'html.parser')
        # Find all of the job listings on the page
        # print(soup)
        job_listings = soup.find_all(data_dict[employer]['jobs_tag'], class_=data_dict[employer]['jobs_class'], id_=data_dict[employer]['jobs_id'])
        
        # # Iterate over each job listing and extract the title, location, and link
        # print(job_listings)
        
        df_old=pd.read_excel('data.xlsx',sheet_name=employer)
        df_job_title=list(df_old['Title'])
        df_job_location=list(df_old['Locations'])
        df_job_url=list(df_old['Url'])
        for job_listing in job_listings:
            # print(job_listing)
            # title = job_listing.find(data_dict[employer]['title_tag'],class_=data_dict[employer]['title_class']).text.strip()
            # location = job_listing.find(data_dict[employer]['location_tag'], class_=data_dict[employer]['location_class']).text.strip()
            # link = job_listing.find(data_dict[employer]['url_tag'])[data_dict[employer]['url_class']]
            
            try:
                title = job_listing.find(data_dict[employer]['title_tag'],class_=data_dict[employer]['title_class']).text.strip()
                df_job_title.append(title)
            except: 
                title=''
                df_job_title.append(title)
            try:
                location = job_listing.find(data_dict[employer]['location_tag'], class_=data_dict[employer]['location_class'],).text.strip()
                df_job_location.append(location)
            except:
                location=''
                df_job_location.append(location)
            try:
                link = job_listing.find(data_dict[employer]['url_tag'])[data_dict[employer]['url_class']]
                df_job_url.append(link)
            except:
                link=''
                df_job_url.append(link)
            # Print the extracted information
            # if title!='' and location!='' and link!='':
            print(f'Title: {title}\nLocation: {location}\nLink: {link}\n')
        df=pd.DataFrame({
            'Title':df_job_title,
            'Locations':df_job_location,
            'Url':df_job_url
        })
        with pd.ExcelWriter("data.xlsx",mode='a',if_sheet_exists='replace') as writer:
            df.to_excel(writer,sheet_name=employer)


# print(job_listings)
