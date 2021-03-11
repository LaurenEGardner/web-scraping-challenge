from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/Wayne Gardner/Desktop/chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrapeMars():
    browser = init_browser()
    #################
    # Scraping news #
    #################
    # Visit the nasa mars news website
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    # Pause for page to load
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    #Assign the text to variables that you can reference later.

    headline = soup.find_all("div", class_="content_title")
    news_title=headline[1].text
    article = soup.find_all("div", class_="article_teaser_body")
    news_p=article[0].text
    
    ###########################
    # Scraping Featured Image #
    ###########################
    #NASA changed website so this doesn't work atm 
    # # Visit the url for JPL Featured Space Image
    # url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # browser.visit(url2)

    # # Pause for page to load
    # time.sleep(1)

    # # Scrape page into Soup
    # html = browser.html
    # soup = bs(html, "html.parser")
    
    # #navigate the site and find the image url for the current Featured Mars Image
    # #and assign the url string to a variable called featured_image_url.
    # relative_image_path = soup.find('article', class_="carousel_item")['style']
    # relative_image_path_url=relative_image_path.split("('", 1)[1].split("')")[0]
    # featured_image_url = "https://www.jpl.nasa.gov/" + relative_image_path_url
    
    ##################
    # Scraping facts #
    ##################
    # Visit the Mars Facts webpage
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)

    # Pause for page to load
    time.sleep(1)

    # Scrape page into Soup
    html3 = browser.html
    soup = bs(html3, "html.parser")
    
    #scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts=soup.find_all(class_="column-2")
    eq_diam=facts[0].text
    polar_diam=facts[1].text
    mass=facts[2].text
    moons = facts[3].text
    orb_dist=facts[4].text
    orb_period=facts[5].text
    surf_temp=facts[6].text
    first_rec=facts[7].text
    rec_by=facts[8].text
    
    
    #building fact table
    mars_facts=[
        {"key" : "Equatorial Diameter", "value" :eq_diam},
        {"key" : "Polar Diameter", "value" :polar_diam},
        {"key" : "Mass", "value" :mass},
        {"key" : "Moons", "value" :moons},
        {"key" : "Orbit Distance", "value" :orb_dist},
        {"key" : "Orbit Period", "value" :orb_period},
        {"key" : "Surface Temp", "value" :surf_temp},
        {"key" : "First Record", "value" :first_rec},
        {"key" : "Recorded By", "value" :rec_by}
    ]

    #######################
    # Scraping Hem images #
    #######################
    # Visit the USGS Astrogeology site 
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    # Pause for page to load
    time.sleep(1)

    # Scrape page into Soup
    html4 = browser.html
    soup = bs(html4, "html.parser")
    
    #obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image
    #for each hemisphere, pull the link to the page, go to that page, find the url
    
    base_url="https://astrogeology.usgs.gov"
    #save all urls for hemisphere image pages to a list, then go to the urls
    #and pull the large image url & add to list
    hemispheres=soup.find_all("a",class_="itemLink product-item")
    total=0
    urls=[]
    hem_imgs=[]
    for hemisphere in hemispheres:
        url=base_url+hemispheres[total].attrs["href"]
        if url not in urls:
            urls.append(url)
        total = total + 1
    for url in urls:
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        hem=soup.find_all("img",class_="wide-image")[0].attrs["src"]
        hem_imgs.append(hem)
        
    
    #hemisphere image table
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": base_url + hem_imgs[3]},
    {"title": "Cerberus Hemisphere", "img_url": base_url + hem_imgs[0]},
    {"title": "Schiaparelli Hemisphere", "img_url": base_url + hem_imgs[1]},
    {"title": "Syrtis Major Hemisphere", "img_url": base_url + hem_imgs[2]},
    ]
    
    # Quit the browser after scraping
    browser.quit()

    mars_data = {
        "news_p": news_p,
        "news_title": news_title,
        "mars_facts" : mars_facts, 
        # "featured_image": featured_image_url,
        "hemisphere_image": hemisphere_image_urls
    }

    # Return results
    return mars_data