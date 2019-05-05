from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #WINDOWS USER
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    news_title = soup.find('h3').text
    news_p = soup.find('div', class_ = 'rollover_description_inner').text
    browser.quit() 

    # MAC USER
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #WINDOWS USER
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    # Visit the url for JPL Featured Space Image 
    nasa_url =  "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    #Retrieve all elements that contain book information
    featured_image_url  = soup.find('div', class_='carousel_container').find('article')['style']
    featured_image_url = featured_image_url[23:-3]
    prefix_url = 'https://www.jpl.nasa.gov'
    featured_image_url = prefix_url + featured_image_url
    browser.quit()    

    twit_url = 'https://twitter.com/marswxreport?lang=en'
    twit_response = requests.get(twit_url)
    twit_soup = BeautifulSoup(twit_response.text, 'html.parser')
    #twit_soup
    mars_weather = twit_soup.find('p', class_="TweetTextSize").text


    twitter_url = 'https://space-facts.com/mars/'
    planet_facts_table = pd.read_html(twitter_url)
    planet_facts_table = planet_facts_table[0]
    planet_facts_table.columns = ['Description', 'Value']
    planet_facts_table = planet_facts_table.set_index('Description')
    #planet_facts_table
    planet_facts_table_html = planet_facts_table.to_html()



    # !which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    # HTML object
    astro_html = browser.html
    #Parse HTML with Beautiful Soup
    astro_soup = BeautifulSoup(astro_html, 'html.parser')
    #astro_soup
    img_links = astro_soup.find_all('h3')
    # img_links

    asto_url_prefix = 'https://astrogeology.usgs.gov/'

    hemisphere_image_urls = []

    for img_link in img_links:
        # image_page = 
        browser.click_link_by_partial_text(img_link.text)
        html= browser.html
        page_soup = BeautifulSoup(html, 'html.parser')
        img_url_suffix = page_soup.find('img', class_='wide-image')['src']
        img_url = asto_url_prefix + img_url_suffix
        title = page_soup.find('h2', class_='title').text
        img_dict = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(img_dict)
        browser.back()
        


    # Store data in a dictionary

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'planet_facts_table_html': planet_facts_table_html,
        'hemisphere_image_urls' : hemisphere_image_urls
    }


     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

