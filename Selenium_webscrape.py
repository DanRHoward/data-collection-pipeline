import json #import to store scrapped data
import numpy as np #import to present all data as a vertical vector array
import os #import to create directories to store data and check if it's empty
import shutil #import to delete non-empty directory
import time #import to create 'sleeper' timers to allow web page to load fully
from selenium import webdriver #imports to allow the web driver to run
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class IMDB_scrape:
    """This class is used to web scrape data from the IMDB webpage dedicated to the top 250 movies of all time.
    
    Parameters
    ----------
    file_path: str
        The file path the user wished to store all the data from the web strape.

    Returns
    -------
    raw_data: dir
        Directory containing all data gathered from web scrape.
    """
    
    def __init__(self,file_path):
        """
        This method is used to initialize the web srape. 
        The url for the web scrape is locally defined and is used to setup the driver which powers the selenium approach to web scraping.
        """
        url = "https://www.imdb.com/chart/top/" #url for our page we want to see
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install())) #setup for driver in windows
        driver.get(url) #load webpage with given url

        self.driver = driver
        self.file_path = file_path
        time.sleep(2) #allow time for the page to load (2 seconds fixed time)

        #self.login_cookies()
        #print(np.array([self.final_list]).T)
        
    def accept_cookies(self): #automatically accept cookies
        """
        This method automatically accepts any cookie notification which may appear on the website.
        """
        try: 
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]') #XPATH to 'accept cookies' button
            accept_cookies_button.click() #click 'accept cookies' button
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def login(self): #automatically login with given username and password
        """
        This method automatically inputs login infomation is required.
        Username and Password obtained from user input.
        If no login is required, simply press eneter when input is prompted.
        """
        #try:
            #username = input("Enter your username (if applicable): ")
            #password = input("Enter your password (if applicable): ")
            # driver.find_element(by=By."method of choice", value="method's value for the username input").send_keys(username)
            # driver.find_element(by=By."method of choice", value="method's value for the password input").send_keys(password)
            # driver.find_element(by=By."method of choice", value="method's value to find login button").click()
        #except:
            #pass

    def login_cookies(self): #method to auto complete logins and accept cookies if they appear
        """
        This method calls the methods login() and accpet_cookies().
        Further info, see login() and accept_cookies().
        """
        try: #if a login is required
            self.login()
            self.accept_cookies()
        except: #if a login is not required
            self.accept_cookies()
        # self.scrape_data()

    def scrape_data(self): #method to scrape relevent data from website
        """
        This method is responsible for scraping the data from the given website. Data collected is stored in individual dictionaries.

        return
        ------
        final_movie_list: list
            Returns list of dictionaries containing relevent data for each movie. 
        """
        self.login_cookies()
        container = self.driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody') #path to body of the table we desire to extract data from
        self.movie_list = container.find_elements(by=By.TAG_NAME, value='tr') #find all the table row 
        self.final_movie_list = [] #list of all the info for each movie
        self.movie_links = [] #list of links for each movie
        rank = 0 #rank of each movie (could not scrape data as no relative path could be found, but movies are already ordered so this method yields the same result)
        for movie in self.movie_list: #"for each table row in the whole table"
            rank += 1 #Had to be done like this as html code had no assigned values to call for
            title_year = movie.find_element(by=By.CLASS_NAME, value='titleColumn') #find the entry corresponding to the 'titleColumn' cell
            name = title_year.find_element(by=By.TAG_NAME, value='a').text #find element with tag name 'a' in previously searched cell, then convert to text
            release_year = title_year.find_element(by=By.CLASS_NAME, value='secondaryInfo').text.replace("(","").replace(")","") #find element corresponding to cell 'secondaryInfo', then replace brackets with nothing
            imdb_rating = movie.find_element(by=By.XPATH, value=f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{rank}]/td[3]/strong').text #Class name was not working so had to use the XPATH this way
    
            movie_page = title_year.find_element(by=By.TAG_NAME, value='a') #search element with tag name of "a" in area defined in 'title_year'
            self.movie_link = movie_page.get_attribute('href') #give us value assigned to 'href' from this element
            self.movie_links.append(self.movie_link) #append movie link to list of movie links

            movie_info = {
                'RANK': rank,
                'TITLE': name,
                'RELEASE YEAR': release_year,
                'IMDB RATING': imdb_rating,
                'IMDB PAGE': self.movie_link
            } #define dictionary with all relevent info about each movie
            #print(self.movie_info)
            self.final_movie_list.append(movie_info) #append each dictionary into a list
        # self.get_posters()
        return self.final_movie_list

    def get_posters(self,index=0):
        """
        This method gathers the info url for the poster of each movie and appends it to the variable final_movie_list.

        return
        ------
        poster_list: list
            List containing each image url for every movie.
        """
        self.scrape_data()
        self.poster_list = [] #initial list of poster urls
        #container = self.driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody') #path to body of the table we desire to extract data from
        #self.movie_data_list = container.find_elements(by=By.TAG_NAME, value='tr') #find all the table row 
        for movie in self.movie_list:
            poster_column_cell = movie.find_element(by=By.CLASS_NAME, value='posterColumn')
            access_poster = poster_column_cell.find_element(by=By.TAG_NAME, value='a')
            find_image = access_poster.find_element(by=By.TAG_NAME,value='img')
            poster = find_image.get_attribute('src')
            self.poster_list.append(poster)
            self.final_movie_list[index]['POSTER'] = poster 
            index += 1
        # self.store_data(self.file_path)
        return self.final_movie_list

    def store_data(self,file_path):
        """
        This method stores the collected data into a created directory.

        return
        ------
        raw_data: dir
            Directory storing all data collected via the scrape_data(), get_poster() and download_poster() method.
        """
        self.get_posters()
        try:
            shutil.rmtree(file_path + "/raw_data")
            print('*'*100)
            print('Directory named \'raw_data\' already exists.')
        except:
            pass
        os.mkdir(file_path + "/raw_data")
        for index in range(250):
            try: #will fail if directory is already present
                if ":" in self.final_movie_list[index]['TITLE']: #since the character ":" cannot be up into a file name, we need to replace it when this character arises
                    altered_title = self.final_movie_list[index]['TITLE'].replace(":",",") #create altered movie title
                    os.mkdir(file_path + f"/raw_data/{altered_title}") #use new title as file name
                else: #if its not in the title
                    os.mkdir(file_path + f"/raw_data/{self.final_movie_list[index]['TITLE']}") #use saved title as name
            except:
                # print(f"Directory named \'{self.final_list[index]['TITLE']}\' already exists.")
                continue
            
            if ":" in self.final_movie_list[index]['TITLE']: #if ":" is present in title
                with open(file_path + f"/raw_data/{altered_title}/data.json", 'w') as f: #follow is path to store data
                    json.dump(self.final_movie_list[index], f) #store data in path
            else: #if ":" is not present
                with open(file_path + f"/raw_data/{self.final_movie_list[index]['TITLE']}/data.json", 'w') as f:   #follow path to store data    
                    json.dump(self.final_movie_list[index], f) #store data in path
        print('Data stored!') #print when all data is stored
        # self.download_posters()
        return self.file_path

    def download_posters(self):
        """
        This method downloads each movie's poster into the directory created with the store_data() method.
        """
        import urllib.request #import to download given image url
        from datetime import date #import to get current years, months and days value
        from time import strftime #import to get current hour, minute and second value
        self.store_data(self.file_path)
        try:
            os.mkdir(self.file_path + "/raw_data/images") #create directory with given path
        except:
            print('Directory named \'images\' already exists.') #if it already exists, prints this instead (no durplicate folder created)
        
        if len(os.listdir(self.file_path + '/raw_data/images')) > 0: #checking if files are present in the directory
            for files in os.listdir(self.file_path + '/raw_data/images'): #for all files in directory...
                os.remove(self.file_path + '/raw_data/images/' + files) #remove them
            print('Files found in \'images\' directory! Files have been deleted and will be replaced.') #print message
        else:    
            print("Directory \'image\' is empty. Procceding with image downloads.") #if directory is empty
        
        for movie_index in range(250): #250 chosen as we have 250 urls in data set
                poster_url = self.poster_list[movie_index] #cycles through each movie's poster url
                image_file_path = self.file_path + "/raw_data/images" #path to folder we want to store the images in
                year, month, day = date.today().year, date.today().month, date.today().day #finds year, month and day of run (type: int)
                hour, minute, second = strftime("%H"), strftime("%M"), strftime("%S") #finds hour, minute and second of run (type: str)
                if len(str(day)) == 1: #adds a zero at the front of the file name (consistant length of file names)
                    day = "0"+str(day)
                file_name = f"/{day}{month}{year}_{hour}{minute}{second}_{movie_index}" #define name dependent of time and index number
                full_path = image_file_path + file_name + ".jpg" #store as .jpg
                urllib.request.urlretrieve(poster_url,full_path) #perfrom the download with the url of the image and the path we want to store it in
        print('Poster images downloaded!')
        return self.file_path

def run_scrape(file_path):
    """
    This function creates an instance of the class with the file path of where all the data is to be stored.

    parameters
    ----------
    file_path: str
        file_path argument for the class 'IMDB_scrape()' to create an instance of the class.
    """
    start_time = time.time() #time that the web scrape was performed
    class_instance = IMDB_scrape(file_path).download_posters() #create instance by assigning class with a variable
    total_time_run = abs(time.time()-start_time) #calculates time since start of the run
    print(f'The web scrape took {int(total_time_run/60)} minute(s), {int(total_time_run % 60)} seconds.') #prints run time
    return class_instance

if __name__ == "__main__":
    run_scrape("C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline")
else:
    print('Code cannot be run as import.')