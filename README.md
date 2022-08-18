# Mission-to-Mars

## Project Overview

The purose of this project is to create a webpage with current information on NASA's mission to the planet Mars.  This project uses webdriver-manager and splinter and BeautifulSoup when webscraping the article, image, and table of facts from various websites, stores the data in a Mongo DB database, then uses the Flask app to create a web app where the information is displayed.  The actual display of the information on the web app employs Bootstrap, HTML, and CSS.  As designed, when the specific source websites update the articles, images, or information on Mars, the most current data gets scraped and displayed onto the Mission-to-Mars webpage.