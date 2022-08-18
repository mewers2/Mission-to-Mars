#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import pandas
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# With the following line, `browser.is_element_present_by_css('div.list_text', wait_time=1)`, we are accomplishing two things.
# 
# One is that we're searching for elements with a specific combination of tag (`div`) and attribute (`list_text`). As an example, `ul.item_list` would be found in HTML as `<ul class="item_list">`.
# 
# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[3]:


# Visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Notice how we've assigned `slide_elem` as the variable to look for the `<div />` tag and its descendent (the other tags within the `<div />` element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The `.` is used for selecting classes, such as `list_text`, so the code `'div.list_text'` pinpoints the `<div />` tag with the class of `list_text`. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using `select_one`, the first matching element returned will be a `<li />` element with a class of `slide` and all nested elements within it.

# In[4]:


# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In this line of code, we chained `.find` onto our previously assigned variable, `slide_elem`. When we do this, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data." The data we're looking for is the content title, which we've specified by saying, "The specific data is in a `<div />` with a class of `'content_title'`."

# In[5]:


# Begin scraping: trying to get the title for the most recent article published on the website.
slide_elem.find('div', class_='content_title')


# We've added something new to our `.find()` method here: `.get_text()`. When this new method is chained onto `.find()`, only the text of the element is returned. The code above, for example, would return only the title of the news article and not any of the HTML tags or elements.

# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# here are two methods used to find tags and attributes with BeautifulSoup:
# 
# `.find()` is used when we want only the first class and attribute we've specified.
# `.find_all()` is used when we want to retrieve all of the tags and attributes.
# For example, if we were to use `.find_all()` instead of `.find()` when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.

# In[7]:


# Use the parent element to find the paragraph text (article summary)
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Notice the indexing chained at the end of the first line of code? With this, we've stipulated that we want our browser to click the second button.

# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Let's break it down:
# 
# An `img` tag is nested within this HTML, so we've included it.
# `.get('src')` pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the `<img />` tag for an image with a class of `fancybox-image`. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."
# 
# This looks great! We were able to pull the link to the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL directly. This way, when JPL updates its image page, our code will still pull the most recent image.
# 
# But if we copy and paste this link into a browser, it won't work. This is because it's only a partial link, as the base URL isn't included. If we look at our address bar in the webpage, we can see the entire URL up there already; we just need to add the first portion to our app

# In[11]:


# Find the relative image URL
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# We're using an f-string for this print statement because it's a cleaner way to create print statements; they're also evaluated at run-time. This means that it, and the variable it holds, doesn't exist until the code is executed and the values are not constant. This works well for our scraping app because the data we're scraping is live and will be updated frequently.

# In[12]:


# Use the bsae URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# Tables in HTML are basically made up of many smaller containers. The main container is the `<table />` tag. Inside the table is `<tbody />`, which is the body of the table—the headers, columns, and rows.
# 
# `<tr />` is the tag for each table row. Within that tag, the table data is stored in `<td />` tags. This is where the columns are established.
# Instead of scraping each row, or the data in each `<td />`, we're going to scrape the entire table with Pandas' `.read_html()` function.
# Remember to make sure you imported the pandas dependency. `import pandas as pd`
# 

# `df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0]` With this line, we're creating a new DataFrame from the HTML table. The Pandas function `read_html()` specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# `df.columns=['description', 'Mars', 'Earth']` Here, we assign columns to the new DataFrame for additional clarity.
# `df.set_index('description', inplace=True)` By using the `.set_index()` function, we're turning the Description column into the DataFrame's index. `inplace=True` means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
# Now, when we call the DataFrame, we're presented with a tidy, Pandas-friendly representation of the HTML table we were just viewing on the website.

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# his is exactly what Robin is looking to add to her web application. How do we add the DataFrame to a web application? Robin's web app is going to be an actual webpage. Our data is live—if the table is updated, then we want that change to appear in Robin's app also.
# 
# Thankfully, Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the `.to_html()` function. 
# 
# The result is a slightly confusing-looking set of HTML code—it's a `<table />` element with a lot of nested elements. This means success. After adding this exact block of code to Robin's web app, the data it's storing will be presented in an easy-to-read tabular format.

# In[14]:


df.to_html()


# Now that we've gathered everything on Robin's list, we can end the automated browsing session. This is an important line to add to our web app also. Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on). We really only want the automated browser to remain active while we're scraping data. It's like turning off a light switch when you're ready to leave the room or home.

# In[15]:


# End the automated browsing session
browser.quit()


# All of the scraping work is coming together. Robin's code can pull article summaries and titles, a table of facts, and a featured image. This is awesome. And Jupyter Notebook is the perfect tool for building a scraping script. We can build it in chunks: one chunk for the image, one chunk for the article, and another for the facts. Each chunk can be tested and run independently from the others. However, we can't automate the scraping using the Jupyter Notebook. To fully automate it, it will need to be converted into a .py file.
# 
# The next step in making this an automated process is to download the current code into a Python file. It won't transition over perfectly, we'll need to clean it up a bit, but it's an easier task than copying each cell and pasting it over in the correct order.
# 
# The Jupyter ecosystem is an extremely versatile tool. We already know many of its great functions, such as the different libraries that work well with it and also how easy it is to troubleshoot code. Another feature is being able to download the notebook into different formats.
# 
# There are several formats available, but we'll focus on one by downloading to a Python file.
# 
# - While your notebook is open, navigate to the top of the page to the Files tab.
# - From here, scroll down to the "Download as" section of the drop-down menu.
# - Select "Python (.py)" from the next menu to download the code.
# - If you get a warning about downloading this type of file, click "Keep" to continue the download. 
# - Navigate to your Downloads folder and open the new file. A brief look at the first lines of code shows us that the code wasn't the only thing to be ported over. The number of times each cell has been run is also there, for example.
# - Clean up the code by removing unnecessary blank spaces and comments.

# # Challenge Code

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[17]:


#html = browser.html
#img_soup = soup(html, "html.parser")
#all_img_bin = img_soup.find_all('div', class_='item')
#all_img_bin[0]('a')[1]['href']
#all_img_bin[1]('a')[1]['href']
#all_img_bin[2]('a')[1]['href']
#all_img_bin[3]('a')[1]['href']


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    #html = browser.html
    #img_soup = soup(html, "html.parser")
    #all_img_bin = img_soup.find_all('div', class_='item')

links = browser.find_by_css('a.product-item img')

# Loop through the links, click the link, find teh sample anchor, and return the href
for x in range(len(links)):
    #ind_img_tag = all_img_bin[x]

    # create an empty dictionary to hold the image url's and titles
    hemispheres = {}

    # scrape the full resolution image URL's
        #ind_img_link = ind_img_tag('a')[1]['href']
        
    # Navigate the browser to the URL
        #browser.visit(ind_img_link)
        #img_html = browser.html
        #img_url_soup = soup(img_html, "html.parser")
    browser.find_by_css('a.product-item img')[x].click()
    
    # Scrape the full resolution image and the image title
        #img_url = img_url_soup.find('a', target='_blank')['href']
        #img_title = img_url_soup.find('h2', class_='title')[text]
    sample_elem = browser.links.find_by_text('Sample').first
    hemispheres['img_url'] = sample_elem['href']
    
    hemispheres['title'] = browser.find_by_css('h2.title').text
    
    
    # Save the image link and title
        #hemispheres['img_url'] = (img_url)
        #hemispheres['title'] = (img_title)
    hemisphere_image_urls.append(hemispheres)

    # Navigate back to get the next image
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




