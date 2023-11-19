from bs4 import BeautifulSoup
import pandas as pd
import os
from lxml import etree
import asyncio
from pyppeteer import launch
data_dict={
    'Southern Company':{ # Doesn't work :(
        'urls':['https://southerncompany.jobs/jobs/?q=nuclear'],
        'title_xpath':'//*[@id="jobs"]/li/section/div/a',
        'location_xpath':'//*[@id="jobs"]/li/section/div/a/div/div',
        'location_place':'',
        'url_xpath':'//*[@id="jobs"]/li/section/div/a'
    },
    'Westinghouse':{#perfect just like you :)
        'urls':
        ['https://careers.westinghousenuclear.com/search/?searchby=location&createNewAlert=false&q=nuclear&locationsearch=&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_city=&optionsFacetsDD_title=&optionsFacetsDD_brand=&optionsFacetsDD_location=']+
        [F"https://careers.westinghousenuclear.com/search/?q=nuclear&searchby=location&d=10&startrow={i}" for i in range(25,475,25)],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a'
    },
    'Duke Energy':{ #Not working
        'urls':['https://dukeenergy.wd1.myworkdayjobs.com'],
        'title_xpath':'//*[@id="mainContent"]',
        'location_xpath':'//*[@class="css-129m7dg"]',
        'location_place':'',
        'url_xpath':'//*[@class="css-19uc56f"]'
    },
    'BWXT':{#Works but URL bug
        'urls':['https://careers.bwxt.com/go/Recent-Grad-and-Student-Jobs/3930400/'],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a'
    },
    'TerraPower':{#Works
        'urls':['https://www.terrapower.com/contact-us/careers/'],
        'title_xpath':'//*[@class="rbox-opening-li-title"]',
        'location_xpath':'//*[@class="rbox-job-shortdesc"]',
        'location_place':'',
        'url_xpath':'//*[@class="rbox-opening-li-title"]'
    },
    'Urenco':{#:(
        'urls':['https://www.urenco.com/careers/vacancies?function%5B%5D=Engineering'],
        'title_xpath':'//*[@id="vacancies-grid"]/div/div/div[1]/div[1]/h3/a',
        'location_xpath':'//*[@id="vacancies-grid"]/div/div/div[2]/div[1]/span',
        'location_place':'',
        'url_xpath':'//*[@id="vacancies-grid"]/div/div/div[1]/div[1]/h3/a'
    },
    'General Atomics':{# Works but needs to read multiple pages
        'urls':['https://www.ga-careers.com/search-jobs/nuclear?orgIds=499&kt=1&ac=376'],
        'title_xpath':'/html/body/div[1]/main/div[1]/div/div[2]/section/section/ul/li/a/h2',
        'location_xpath':'/html/body/div[1]/main/div[1]/div/div[2]/section/section/ul/li/a/span[2]',
        'location_place':'',
        'url_xpath':'/html/body/div[1]/main/div[1]/div/div[2]/section/section/ul/li/a'
    },
    'Entergy':{#Works but has the url bug
        'urls':['https://jobs.entergy.com/search/?createNewAlert=false&q=nuclear&locationsearch='],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[3]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a'
        },
    'Orano':{#Doesn't work :(
        'urls':['https://www.orano.group/jobs/en/our-offers?Keywords=nuclear','https://www.orano.group/jobs/en/our-offers?Page=2&Keywords=nuclear'],
        'title_xpath':'//*[@class="result-item"]/div[1]/div[1]/h3',
        'location_xpath':'//*[@id="app"]/div/div[3]/main/div[2]/div[2]/div[2]/ul/li/div[1]/div[1]/div/div[2]',
        'location_place':'',
        'url_xpath':'//*[@id="app"]/div/div[3]/main/div[2]/div[2]/div[2]/ul/li/div[3]/a'  
    },
    # 'Cameco':{ # Need to add multiple pages
    #     'urls':['https://career17.sapsf.com/career?company=Cameco&career%5fns=job%5flisting%5fsummary&navBarLevel=JOB%5fSEARCH&_s.crb=WXl0EKE4OuePFGQ%2f4phs%2boAy6K1hlTLbgup0a8Vj%2bTc%3d'],
    #     'title_xpath':'',
    #     'location_xpath':'',
    #     'location_place':'',
    #     'url_xpath':'' 
    # },
    'GE Hitachi NE':{ # Works but need to figure out location
        'urls':
        ['https://jobs.gecareers.com/power/global/en/ge-hitachi-nuclear-energy?s=1&rk=l-ge-hitachi-nuclear-energy']+
        [F'https://jobs.gecareers.com/power/global/en/ge-hitachi-nuclear-energy?from={i}&s=1&rk=l-ge-hitachi-nuclear-energy' for i in range(20,100,20)],
        'title_xpath':'/html/body/div[2]/div[2]/div/div/div/div[2]/section[3]/div/div/div/div[1]/div[2]/div[2]/ul/li/div/span/a/div/span',
        'location_xpath':'//*[@class="job-info"]/span[8]/span',
        'location_place':'',
        'url_xpath':'/html/body/div[2]/div[2]/div/div/div/div[2]/section[3]/div/div/div/div[1]/div[2]/div[2]/ul/li/div/span/a'
    },
    'Enercon':{#Works but doesnt read all jobs from the url
        'urls':['https://phe.tbe.taleo.net/phe03/ats/careers/v2/searchResults?org=ENERCON2&cws=37'],
        'title_xpath':'//*[@id="oracletaleocwsv2-wrapper"]/section[5]/div/div/div[2]/div/div/div/div[1]/div[2]/h4/a',
        'location_xpath':'//*[@id="oracletaleocwsv2-wrapper"]/section[5]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]',
        'location_place':'',
        'url_xpath':'//*[@id="oracletaleocwsv2-wrapper"]/section[5]/div/div/div[2]/div/div/div/div[1]/div[2]/h4/a' 
    },
    'FirstEnergy':{#BUST
        'urls':['https://careers.firstenergycorp.com/#en/sites/FirstEnergyCareers/requisitions?keyword=intern&mode=location'],
        'title_xpath':'/html/body/div[4]/div[1]/div/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div/div[2]/div/div/ul/li/div/a/div/search-result-item-header/div/span',
        'location_xpath':'/html/body/div[4]/div[1]/div/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div/div[2]/div/div/ul/li/div/a/div/search-result-item-header/div/span',
        'location_place':'',
        'url_xpath':'/html/body/div[4]/div[1]/div/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div/div[2]/div/div/ul/li/div/a/div/search-result-item-header/div/span'
    },
    'NextEra':{#DONE just needs the url intro
        'urls':['https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/',
                'https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/25/?q=&sortColumn=referencedate&sortDirection=desc',
                'https://jobs.nexteraenergy.com/go/Nuclear-Jobs/2674300/50/?q=&sortColumn=referencedate&sortDirection=desc'],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[1]/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[1]/a'
    },
    'Constellation Energy':{#Need to fix location
        'urls':[F'https://jobs.constellationenergy.com/jobs/search?location=&page={i}&q=nuclear#' for i in range(17)],
        'title_xpath':'//*[@id="the-results"]/div[2]/div/div[3]/div[3]/div/div/div[1]/strong/a',
        'location_xpath':'//*[@id="the-results"]/div[2]/div/div[3]/div[3]/div/div/div[2]',
        'location_place':'',
        'url_xpath':'//*[@id="the-results"]/div[2]/div/div[3]/div[3]/div/div/div[1]/strong/a'   
    },
    'Engie':{#DONE just url needs jobs.engie.com
        'urls':['https://jobs.engie.com/search/?createNewAlert=false&q=nuclear&locationsearch=']+
            [F'https://jobs.engie.com/search/?q=nuclear&startrow={i}' for i in range(25,150,25)],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[1]/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/div/span[1]/a'
    },
    'Framatone':{#BRUH
        'urls':['https://www.framatome.com/en/jobseekers/job-offers/'],
        'title_xpath':'/html/body/div[4]/main/div/div/div/div/div/div[2]/div[3]/div/div/div/div[1]/a/h2',
        'location_xpath':'/html/body/div[4]/main/div/div/div/div/div/div[2]/div[3]/div/div/div/div[4]',
        'location_place':'',
        'url_xpath':'/html/body/div[4]/main/div/div/div/div/div/div[2]/div[3]/div/div/div/div[1]/a/h2'
    },
    'Idaho NL':{ #BRUUHHHH
        'urls':['https://inl.taleo.net/careersection/inl_external/jobsearch.ftl?lang=en&portal=8110010144#'],
        'title_xpath':'//*[@class="jobsbody"]/tr',
        # 'title_xpath':'/html/body/div[3]/div/div[3]/div[5]/div[3]/div[3]/div[3]/div[2]/table/tbody/tr/th/div/div/span/a',
        'location_xpath':'',
        'location_place':'Idaho',
        'url_xpath':'/html/body/div[3]/div/div[3]/div[5]/div[3]/div[3]/div[3]/div[2]/table/tbody/tr[1]/th/div/div/span/a'
    },
    'Oak Ridge National Lab':{#Works just need to fix the url header
        'urls':['https://jobs.ornl.gov/search/?q=nuclear&searchby=location&d=10',]+
        [F'https://jobs.ornl.gov/search/?q=nuclear&searchby=location&d=10&startrow={i}' for i in range(25,100,25)],
        'title_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',
        'location_xpath':'//*[@id="searchresults"]/tbody/tr/td[2]/span',
        'location_place':'',
        'url_xpath':'//*[@id="searchresults"]/tbody/tr/td[1]/span/a',  
    },
    'Lawrence Livermore NL':{# Doesn't work
        'urls':['https://www.llnl.gov/join-our-team/careers/find-your-job/156da5cf-5933-4153-874f-cfd786065564/nuclear'],
        'title_xpath':'//*[@id="onelab-content"]/div/div/div/div/div/div/div/a[1]',
        # 'location_xpath':'//*[@id="onelab-content"]/div/div[3]/div[2]/div[1]/div/div/small[2]/i',
        'location_xpath':'',
        'location_place':'Livermore, CA',
        'url_xpath':'//*[@id="onelab-content"]/div/div/div/div/div/div/div/a[1]',  
    },
    'Sandia NL':{#has issues
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
    'Helion Fusion':{#DONE
        'urls':['https://www.helionenergy.com/careers/'],
        'title_xpath':'//*[@id="job-list-table"]/li/div/p',
        'location_xpath':'',
        'location_place':'Everett, WA',
        'url_xpath':'//*[@id="job-list-table"]/li/div/div/a',
    },
    'Brookhaven NL':{#Works but with url header issue
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
async def get_html(url):
    # browser = await launch(headless=True, executablePath='/usr/bin/chromium-browser' )  # Launch a headless Chromium browser.
    browser = await launch(headless=True )  # Launch a headless Chromium browser.
    page = await browser.newPage()
    await page.goto(url)  # Navigate to the URL you want to scrape.
    html = await page.content()  # Get the HTML content of the page.
    await browser.close()  # Close the browser when you're done.

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
        try:
            with pd.ExcelWriter('data.xlsx',engine='openpyxl',mode='a',if_sheet_exists='replace') as writer:
                df_test.to_excel(writer,sheet_name=key_list[i],index=False)
        except:
            with pd.ExcelWriter('data.xlsx',engine='openpyxl',mode='w') as writer:
                df_test.to_excel(writer,sheet_name=key_list[i],index=False)
            
init_files()


for employer in list(data_dict.keys())[::-1]:
# for employer in ['General Atomics']:
    url_ind=0
    for url in data_dict[employer]['urls']:
        print(employer)
        url_ind+=1
        # driver=webdriver.Chrome('chromedriver.exe')
        # driver.get(url)
        
        # html = driver.execute_script("return document.documentElement.innerHTML")
        # html=driver.page_source
        
        # driver.quit()

        # Send a GET request to the URL and parse the HTML using BeautifulSoup
        # f=open('test.txt','r')
        # html=f.read()
        # f.close()

        html=asyncio.get_event_loop().run_until_complete(get_html(url))
        soup = BeautifulSoup(html, 'html.parser')
        soup.find_all(data_dict)
        dom = etree.HTML(str(soup))

        # print(job_listings[0].get('href'))
        
        df_old=pd.read_excel('data.xlsx',sheet_name=employer)
        df_job_title=list(df_old['Title'])
        df_job_location=list(df_old['Locations'])
        df_job_url=list(df_old['Url'])
        # print(len(job_listings))
        print(dom.xpath(data_dict[employer]['title_xpath']))
        df_job_title=df_job_title+[i.text for i in dom.xpath(data_dict[employer]['title_xpath'])]
        if data_dict[employer]['location_xpath']=='':
            df_job_location=df_job_location+[data_dict[employer]['location_place']]*len(dom.xpath(data_dict[employer]['title_xpath']))
        else:
            df_job_location=df_job_location+[i.text for i in dom.xpath(data_dict[employer]['location_xpath'])]
        df_job_url=df_job_url+[i.get('href') for i in dom.xpath(data_dict[employer]['url_xpath'])]

        for ind,job_url in enumerate(df_job_url):
            if 'https://' in job_url:
                continue
            else:
                df_job_url[ind]=url.split('/')[0] + '//' + url.split('/')[2] + job_url

        # print('Titles:')
        # for i in df_job_title:
        #     print(i)
        # print('Locations:')
        # for i in df_job_location:
        #     print(i)
        # print('urls')
        # for i in df_job_url:
        #     print(i)
        
        print(len(df_job_title),len(df_job_location),len(df_job_url))
        print('title: ',df_job_title,
              '\nlocation: ',df_job_location,
              '\nurl: ',df_job_url)
        try:
            df=pd.DataFrame({
                'Title':df_job_title,
                'Locations':df_job_location,
                'Url':df_job_url
            })
        except:
            df=pd.DataFrame({
                'Title':[],
                'Locations':[],
                'Url':[]
            })
        with pd.ExcelWriter("data.xlsx",mode='a',if_sheet_exists='replace') as writer:
            df.to_excel(writer,sheet_name=employer,index=False)


# print(job_listings)