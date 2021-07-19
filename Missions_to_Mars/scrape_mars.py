from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # redplanetscience.com
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get news title and paragraph text
    news_title = soup.find('div', class_='content_title').text
    paragraph_text= soup.find('div', class_='article_teaser_body').text

    #JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    featured_image_url = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url=url+featured_image_url

    #Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    
    tables = pd.read_html(url)
    mars_df = tables[1]
    mars_df.columns = ['Desc','Detail']

    desc = mars_df['Desc'].tolist()
    detail = mars_df['Detail'].tolist()

    #list of dictionaries
    table_dict = []
    hemisphere_image_urls = []

    for i, j in zip(desc, detail):
        table_dict.append({"Desc": i, "Data": j})
    table_dict
    
    html_table = mars_df.to_html()
    html_table.replace('\n', '')
    mars_df.to_html('table.html')
    
    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    aes = soup.find_all('a',class_='itemLink product-item',href=True)
    links=[]
    title=[]
    img_url=[]

    #create list of url to cycle to later
    for ae in aes:
        if (ae.img):
            links.append(ae['href'])
    
    for link in links:
        url = 'https://marshemispheres.com/' + link
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        page_title = soup.find('h2',class_='title')
        title.append(page_title.text)
        img_links = soup.find_all('a',target='_blank')
        for img_link in img_links:
            if (img_link.text=='Sample'):
               img_url.append('https://marshemispheres.com/'+img_link['href'])
    
    #list of dictionaries
    hemisphere_image_urls = []

    for i, j in zip(title, img_url):
        hemisphere_image_urls.append({"title": i, "img_url": j})
    # Close the browser after scraping
    browser.quit()
    mars={
        "news_title":news_title,
        "paragraph_text":paragraph_text,
        "featured_image_url":featured_image_url,
        "table":table_dict,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    # Return results
    return mars