# Import Splinter and BeautifulSoup
from types import new_class
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Initiate headless driver for deployment / Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemispheres_images(browser)
        }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the Mars NASA news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=3)


    # Set up the HTML parser: Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')


        # Begin scraping: trying to get the title for the most recent article published on the website.
        # slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text (article summary)
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    
    return news_title, news_p


# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 

        # Find the relative image URL
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None


    # Use the bsae URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    
    
    return img_url


# ## Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:

        # use `read_html` to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    

    # Convert DataFrame back into HTML format using the `.to_html()` function, add bootstrap
    return df.to_html(classes="table table-striped")

### Hemisphere Images

def hemispheres_images(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    links = browser.find_by_css('a.product-item img')

    # Loop through the links, click the link, find teh sample anchor, and return the href
    for x in range(len(links)):
        # create an empty dictionary to hold the image url's and titles       
        hemispheres = {}
        
        # Navigate the browser to the URL
        browser.find_by_css('a.product-item img')[x].click()

        # Scrape the full resolution image and the image title
        sample_elem = browser.links.find_by_text('Sample').first
        hemispheres['img_url'] = sample_elem['href']

        hemispheres['title'] = browser.find_by_css('h2.title').text
    
        # Save the image link and title
        hemisphere_image_urls.append(hemispheres)

        # Navigate back to get the next image
        browser.back()


    return hemisphere_image_urls



if __name__ == "__main__":


    # If running as script, print scraped data
    print(scrape_all())
