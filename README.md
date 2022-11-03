# Data Collection Pipeline

The following project requires the creation of an environment with the certain packages. This list of requirements can be found in 'requirements.txt'.

## Web scrapping using Beautiful Soup

The first stage of this project was to create a simple web scrapping program to gather data from a pre-determined website using Beautiful Soup. Beautiful Soup is a Python library used to pull data out of HTML and XML files. In our case, we access the HTML code for the desired website and use this to navigate its source to extract data we need. The data that was used is in regards to the All-time leading goal scorers of the English Premier League. This code can be found in the file 'WebsiteScrapeStart.py'. Further infomation regarding Beautiful Soup can be found at the following website:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Web scrapping using Selenium

We were then tasked with performing web scrapping using a different method for aquiring data. This new approach was Selenium. Selenium is a tool used to automatically control a web browser. With this automation, we are able to command it to navigate the web page, click on buttons which we need and to gather data via the html source code of the given page. With this, we are able to automate the navigation of potentially hundreds of different websites and gather data from each of them to create a database from this sources. The code which implements this can be found in file 'Selenium.py'. When looking at the code, note that this code only works when running Microsoft Edge. Further infomation regarding Selenium can be found at the following website:

https://selenium-python.readthedocs.io/
