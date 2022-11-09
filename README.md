# Data Collection Pipeline

The following project requires the creation of an environment with the certain packages. This list of requirements can be found in 'requirements.txt'.

## Web scrapping using Beautiful Soup

The first stage of this project was to create a simple web scrapping program to gather data from a pre-determined website using Beautiful Soup. Beautiful Soup is a Python library used to pull data out of HTML and XML files. In our case, we access the HTML code for the desired website and use this to navigate its source to extract data we need. The data that was used is in regards to the All-time leading goal scorers of the English Premier League. This code can be found in the file 'WebsiteScrapeStart.py'. Further infomation regarding Beautiful Soup can be found at the following website:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Web scrapping using Selenium

We were then tasked with performing web scrapping using a different method for aquiring data. This new approach was Selenium. Selenium is a tool used to automatically control a web browser. With this automation, we are able to command it to navigate the web page, click on buttons which we need and to gather data via the html source code of the given page. With this, we are able to automate the navigation of potentially hundreds of different websites and gather data from each of them to create a database from this sources. The code which implements this can be found in file 'Selenium.py'. When looking at the code, note that this code only works when running Microsoft Edge. Further infomation regarding Selenium can be found at the following website:

https://selenium-python.readthedocs.io/

## Structure of the code

Within the web scrape class, all the methods required for this project are defined. Before data collection can begin, we must ensure that the chosen webpage is in the correct state. ie we must deal with any cookie notifications or (if required) login infomation to be input. both of these methods are coalated into a single method named 'login_cookies()'. Once this has been called the data collection begins, with the logic being defined within the mehtod 'scrape_data()'. Each item's data is stored within a dictionary, which are inturn stored inside a list so as to call upon them later. Image data is also collected within the method 'get_posters()' and 'download_posters()'. These methods collect the image urls of each item and, download the images as .jpeg files which are then stored in directories created automatically within the code, respectively. Finally, the code is applied with a conditional check that will only run if:

'''
__name__ == "__main__"
'''

This criterea is known to refer to whether the code is run as a script. If the code is, then the above statement is assigned a value = True, and thus the web scrape is run.

A complication arose when creating a method to store each data group into their own directories with the name of these being the title of each movie. However, certain movies contain the colon character, ":". This character is not allowed to be used for naming directories and thus an error message was produced when the script was run. To fix this, we simply created a variable to store alternative title which replace the colon character with the comma symbol, ",".

## Optional changes

Along with the compulsory elements of the project, optional additions were make to improve the experience. One simple addition is the inclusion of several print() statements which returns a message notifying which stage the data extraction is currently at. A timer was also incorporated which notifies the user how long the script ran until it ended. along with these, a system was created to ensure that duplicate .jpeg files were created within the chosen directory. The quickest solution to create was to simple empty the directory before downloading the new set of images, with updated file names dependent upon the time and date of the download.

## Unit testing

Once the code for the web scrape was completed, the next component of the project was to create and perform unit testing on each of the methods within the web scraper class. These tests are defined within there own class located in file 'Unit_Tests.py'. The test file imports the code for the web scraper, then creates an instance of the class which is used in each test method to verify that the chosen tests are true. For instance, the test_data_scrape() checks whether the output of the method is in the form of a list, that the list elements are dictionaries and that these dictionaries are of length 5. Alterations had to be made within the web scraper code so as to perform these unit tests. To avoid confusion when importing the file using the file's name, the code for the updated web scraper is found in 'Selenium_webscrape.py'.
