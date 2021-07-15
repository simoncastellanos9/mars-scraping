from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    # Set up Splinter
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    paragraph_text= soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(paragraph_text)
    # Close the browser after scraping
    browser.quit()

    # Return results
    return news_title
