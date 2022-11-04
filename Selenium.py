from selenium import webdriver #imports to allow the web driver to run
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time #import to create 'sleeper' timers to allow web page to load fully
import numpy as np #import to present all data as a vertical vector array
import os #import to create directories to store data
import json #import to store scrapped data

class IMDB_scrape:
    def __init__(self):
        url = "https://www.imdb.com/chart/top/" #url for our page we want to see
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install())) #setup for driver in windows
        driver.get(url) #load webpage with given url

        self.driver = driver
        time.sleep(2) #allow time for the page to load

        self.login_cookies() #calling all methods
        self.scrape_data()
        self.get_posters()
        self.store_data()
        self.download_posters()
        #print(np.array([self.final_list]).T)

    def accept_cookies(self): #automatically accept cookies
        try: 
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            self.accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]') #XPATH to 'accept cookies' button
            self.accept_cookies_button.click() #click 'accept cookies' button
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def login(self): #automatically login with given username and password
        self.username = "Username"
        self.password = "Password"
        # If login was required
        # driver.find_element(by=By."method of choice", value="method's value for the username input").send_keys(self.username)
        # driver.find_element(by=By."method of choice", value="method's value for the password input").send_keys(self.password)
        # driver.find_element(by=By."method of choice", value="method's value to find login button").click()
        return 

    def login_cookies(self): #method to auto complete logins and accept cookies if they appear
        try:
            self.login()
            self.accept_cookies()
        except:
            self.accept_cookies()

    def scrape_data(self): #method to scrape relevent data from website
        self.container = self.driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody') #path to body of the table we desire to extract data from
        self.movie_list = self.container.find_elements(by=By.TAG_NAME, value='tr') #find all the table row 
        self.final_list = [] #list of all the info for each movie
        self.movie_links = [] #list of links for each movie
        self.rank = 0
        for movie in self.movie_list:
            self.rank += 1 #Had to be done like this as html code had no assigned values to call for
            self.title_year = movie.find_element(by=By.CLASS_NAME, value='titleColumn') #find the entry corresponding to the 'titleColumn' cell
            self.name = self.title_year.find_element(by=By.TAG_NAME, value='a').text #find element with tag name 'a' in previously searched cell, then convert to text
            self.release_year = self.title_year.find_element(by=By.CLASS_NAME, value='secondaryInfo').text.replace("(","").replace(")","") #find element corresponding to cell 'secondaryInfo', then replace brackets with nothing
            self.imdb_rating = movie.find_element(by=By.XPATH, value=f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{self.rank}]/td[3]/strong').text #Class name was not working so had to use the XPATH this way
    
            self.movie_page = self.title_year.find_element(by=By.TAG_NAME, value='a') #search element with tag name of "a" in area defined in 'title_year'
            self.movie_link = self.movie_page.get_attribute('href') #give us value assigned to 'href' from this element
            self.movie_links.append(self.movie_link) #append movie link to list of movie links

            movie_info = {
                'RANK': self.rank,
                'TITLE': self.name,
                'RELEASE YEAR': self.release_year,
                'IMDB RATING': self.imdb_rating,
                'IMDB PAGE': self.movie_link
            } #define dictionary with all relevent info about each movie
            #print(self.movie_info)
            self.final_list.append(movie_info) #eppend each dictionary into a list
        return # print(self.final_list)

    def get_posters(self,index=0):
        self.poster_list = []
        self.container = self.driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody') #path to body of the table we desire to extract data from
        self.movie_list = self.container.find_elements(by=By.TAG_NAME, value='tr') #find all the table row 
        for movie in self.movie_list:
            poster_column_cell = movie.find_element(by=By.CLASS_NAME, value='posterColumn')
            access_poster = poster_column_cell.find_element(by=By.TAG_NAME, value='a')
            find_image = access_poster.find_element(by=By.TAG_NAME,value='img')
            poster = find_image.get_attribute('src')
            self.poster_list.append(poster)
            self.final_list[index]['POSTER'] = poster 
            index += 1
        return self.poster_list, self.final_list

    def store_data(self):
        try:
            os.mkdir("C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data")
        except:
            print('Directory already exists.')
        for index in range(250):
            try:
                if ":" in self.final_list[index]['TITLE']:
                    altered_title = self.final_list[index]['TITLE'].replace(":",",")
                    os.mkdir(f"C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/{altered_title}")
                else:
                    os.mkdir(f"C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/{self.final_list[index]['TITLE']}")
            except:
                # print(f"Directory named \'{self.final_list[index]['TITLE']}\' already exists.")
                continue
            
            if ":" in self.final_list[index]['TITLE']:
                with open(f"C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/{altered_title}/data.json", 'w') as f:      
                    json.dump(self.final_list[index], f)
            else:
                with open(f"C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/{self.final_list[index]['TITLE']}/data.json", 'w') as f:      
                    json.dump(self.final_list[index], f)
        return print('Data stored!')

    def download_posters(self):
        import urllib.request
        from datetime import date
        from time import strftime
        try:
            os.mkdir(f"C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/images")
        except:
            print('Directory named \'images\' already exists.')
        for index in range(250):
            poster_url = self.poster_list[index]
            file_path = "C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline/raw_data/images" #path to foler we want to store the images in
            year, month, day = date.today().year, date.today().month, date.today().day
            hour, minute, second = strftime("%H"), strftime("%M"), strftime("%S")
            if len(str(day)) == 1: #adds a zero at the front of the file name (consistant length of file names)
                day = "0"+str(day)
            file_name = f"/{day}{month}{year}_{hour}{minute}{second}_{index}" #define name dependent of time and index number
            full_path = file_path + file_name + ".jpg" #store as .jpg
            urllib.request.urlretrieve(poster_url,full_path) #perfrom the download with the url of the image and the path we want to store it in
        return

def run_scrape(): 
    start_time = time.time()
    class_instance = IMDB_scrape() #create instance by assigning class with a variable
    total_time_run = abs(time.time()-start_time)
    print(f'The web scrape took {int(total_time_run)} seconds.')
    return class_instance

if __name__ == "__main__": #check if the code is being run as a script or as an import
    run_scrape() #call function
else:
    print('Code not run as a script!')