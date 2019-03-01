from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
twitter_url = 'https://twitter.com/marswxreport?lang=en'
mars_facts_url = 'https://space-facts.com/mars/'
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def scrape():
	browser = Browser('chrome', headless=False)

	browser.visit(mars_url)
	time.sleep(5)    

	mars_soup = BeautifulSoup(browser.html, 'html.parser')

	title_search = mars_soup.find_all('div', class_ = 'content_title')
	p_search = mars_soup.find_all('div', class_= 'article_teaser_body')

	news_title = title_search[0].text
	paragraph = p_search[0].text

	browser.visit(jpl_url)

	jpl_soup = BeautifulSoup(browser.html, 'html.parser')

	jpl_page = jpl_soup.find_all('a', class_ = 'button fancybox')

	featured_image_url = browser.url + jpl_page[0].attrs['data-fancybox-href']

	browser.visit(twitter_url)

	twitter_soup = BeautifulSoup(browser.html, 'html.parser')

	mars_weather = twitter_soup.find_all('div', class_ = 'tweet')[0].find_all('p')[0].text

	browser.visit(mars_facts_url)

	mars_table = pd.read_html(browser.html)[0]

	mars_table.to_html('table.html')

	browser.visit(usgs_url)

	hemisphere_image_urls = [
    	{"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    	{"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    	{"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    	{"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
	]

	final_dict ={
		'news_title' : news_title,
    	'paragraph' : paragraph,
    	'featured_image_url' : featured_image_url,
    	'mars_weather' : mars_weather,
    	'mars_table' :mars_table,
    	'hemisphere_images' : hemisphere_image_urls}

	return final_dict