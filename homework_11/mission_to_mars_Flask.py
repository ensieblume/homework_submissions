import pandas as pd
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from flask import Flask, Markup, render_template

# Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mission_to_mars_db

#* Use FLASK to create your routes.
@app.route("/")
def display_page():
    db_list = list(db.mission_to_mars.find())
    db_dict = db_list[0]
    print(db_dict)

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", inventory=db_dict)

@app.route("/scrape")
def scrape_and_save():
    # Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
    # Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks.
    # The following outlines what you need to scrape.

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    # Assign the text to variables that you can reference later.

    # Example:
    # news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"

    # news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer,
    #          on course for launch next May from Vandenberg Air Force Base in central California 
    #          -- the first interplanetary launch in history from America's West Coast."

    # First site:
    # https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    list_text = soup.find('div', class_= 'list_text')
    list_text

    title = soup.find('div', class_='content_title')
    title

    latest_news_title = title.find('a').text
    latest_news_title

    latest_news_paragraph = soup.find('div', class_='article_teaser_body').text
    latest_news_paragraph

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string
    # to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'


    # In[12]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    full_image = soup.find('a', class_='button fancybox')
    full_image

    full_image_url = full_image['data-fancybox-href']
    full_image_url

    featured_image_url = 'https://www.jpl.nasa.gov' + full_image['data-fancybox-href']
    featured_image_url

    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    # Save the tweet text for the weather report as a variable called mars_weather.
    # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url) 

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweets = soup.find_all('li', class_='js-stream-item')
    # tweets

    # Find the latest tweet by 'Mars Weather', i.e. not a retweet
    for tweet in tweets:
        if tweet.find('a', class_='account-group', href='/MarsWxReport'):
            break
    author_block = tweet.find('span', class_='FullNameGroup')
    author_block.text

    text_container = tweet.find('div', class_='js-tweet-text-container')
    text_container

    mars_weather = text_container.text.strip()
    mars_weather

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    # including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'

    # Use the read_html function in Pandas to automatically scrape any tabular data from a page.
    tables = pd.read_html(url)
    tables

    type(tables)

    df = tables[0]
    df.columns = ['Facts about Mars', 'info']
    df

    type(df)

    html_table = df.to_html(index=False)
    html_table

    # Strip unwanted newlines to clean up the table
    html_table.replace('\n', '')

    df.to_html('table.html', index=False)

    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary
    # for each hemisphere.
    # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    #]

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find_all('div', class_='description')
    divs

    hemisphere_image_urls = []
    for div in divs:
        link = div.find('a')
        href = 'https://astrogeology.usgs.gov' + link['href']
        title = div.find('h3').text
        hemisphere_image_urls.append({'title': title, 'pageURL': href})
        print(hemisphere_image_urls)

    for hemisphere_image_url in hemisphere_image_urls:
        url = hemisphere_image_url['pageURL']
        print(url)
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', class_='downloads')
        image_a = div.find('a', text='Sample')
        print(image_a)
        image_link = image_a['href']
        print(image_link + "\n")
        hemisphere_image_url['img_url'] = image_link
    print(hemisphere_image_urls)


    # Drops collection if available to remove duplicates
    db.mission_to_mars.drop()

    # Creates a collection in the database and inserts two documents
    dict = {}
    dict['latest_news_title'] = latest_news_title
    dict['latest_news_paragraph'] = latest_news_paragraph

    dict['featured_image_url'] = featured_image_url

    dict['mars_weather'] = mars_weather
    dict['html_table'] = Markup(html_table)

    dict['hemisphere_0_title'] = hemisphere_image_urls[0]['title']
    dict['hemisphere_0_img_url'] = hemisphere_image_urls[0]['img_url']
    dict['hemisphere_1_title'] = hemisphere_image_urls[1]['title']
    dict['hemisphere_1_img_url'] = hemisphere_image_urls[1]['img_url']
    dict['hemisphere_2_title'] = hemisphere_image_urls[2]['title']
    dict['hemisphere_2_img_url'] = hemisphere_image_urls[2]['img_url']
    dict['hemisphere_3_title'] = hemisphere_image_urls[3]['title']
    dict['hemisphere_3_img_url'] = hemisphere_image_urls[3]['img_url']
    print(dict)
    db.mission_to_mars.insert_one(dict)

    return (
        f"Done<br/>"
    )

# With debug=True, Flask server will auto-reload when there are code changes
if __name__ == '__main__':
	app.run(debug=True)
