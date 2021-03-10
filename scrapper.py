from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time, csv
import requests

startUrl = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome(r'C:/Users/siddh/Downloads/chromedriver/chromedriver.exe')
browser.get(startUrl)
time.sleep(10)

headers = ['Name', 'Light_Years_From_Earth', 'Planet_Mass', 'Stellar_Magnitude', 'Discovery_Date', 'Hyperlink', 'Planet_Type', 'Planet_Radius', 'Orbital_Radius', 'Orbital_Perios', 'Eccentricity']
planetData = []
extraPlanetData = []


def scrapper():
    
    for i in range(0, 437):
        soup = bs(browser.page_source, 'html.parser')

        for ul_tag in soup.find_all('ul', attrs = {'class', 'exoplanet'}):

            li_tags = ul_tag.find_all('li')
            tempList = []

            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    tempList.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        tempList.append(li_tag.contents[0])
                    except:
                        tempList.append('')
        
            hyperlink_litag = li_tags[0]    
            tempList.append('https://exoplanets.nasa.gov/' + hyperlink_litag.find_all('a', href = True)[0]['href'])
            planetData.append(tempList)        

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()




def scrapData(hyperlink):

    try:


        page = requests.get(hyperlink)
        soup = bs(page.content, 'html.parser')

        for tr_tag in soup.find_all('tr', attrs = {'class': 'fact_row'}):
            td_tags = tr_tag.find_all('td')
            temp = []

            for td_tag in td_tags:
                try:
                    temp.append(td_tag.find_all('div', attr = {'class': 'value'})[0].contents[0])
                except:
                    temp.append('')
            
            extraPlanetData.append(temp)
    
    except:
        time.sleep(1)
        scrapData(hyperlink)


scrapper()

for data in planetData:
    scrapData(data[5])


finalPlanetData = []

for index, data in enumerate(planetData):
    finalPlanetData.append(data + extraPlanetData[index])

with open('final.csv', 'w') as f:
    csvwriter = csv.writer(f) 
    csvwriter.writerow(headers)
    csvwriter.writerows(finalPlanetData)