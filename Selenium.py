from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class IMDB_scrape:
    def __init__(self):
        url = "https://www.imdb.com/chart/top/"
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.get(url)

        self.driver = driver
        time.sleep(2)

        self.login_cookies()
        self.scrape_data()
    
    def accept_cookies(self):
        try: 
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            self.accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]') #XPATH to 'accept cookies' button
            self.accept_cookies_button.click() #click 'accept cookies' button
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def login(self):
        self.username = "Username"
        self.password = "Password"
        # If login was required
        # driver.find_element(by=By."method of choice", value="method's value for the username input").send_keys(username)
        # driver.find_element(by=By."method of choice", value="method's value for the password input").send_keys(password)
        # driver.find_element(by=By."method of choice", value="method's value to find login button").click()
        return 

    def login_cookies(self):
        try:
            self.login()
            self.accept_cookies()
        except:
            self.accept_cookies()

    def scrape_data(self):
        self.container = self.driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody') #List path
        self.movie_list = self.container.find_elements(by=By.TAG_NAME, value='tr')
        self.final_list = []
        self.movie_links = []
        self.rank = 0
        for movie in self.movie_list:
            self.rank += 1 #Had to be done like this as html code had no assigned values to call for
            self.title_year = movie.find_element(by=By.CLASS_NAME, value='titleColumn')
            self.name = self.title_year.find_element(by=By.TAG_NAME, value='a').text
            self.release_year = self.title_year.find_element(by=By.CLASS_NAME, value='secondaryInfo').text.replace("(","").replace(")","")
            self.imdb_rating = movie.find_element(by=By.XPATH, value=f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{self.rank}]/td[3]/strong').text #Class name was not working so had to use the XPATH this way
    
            self.movie_page = self.title_year.find_element(by=By.TAG_NAME, value='a') #search element with tag name of "a" in area defined in 'title_year'
            self.movie_link = self.movie_page.get_attribute('href') #give us value assigned to 'href' from this element
            self.movie_links.append(self.movie_link)

            movie_info = {
                "Rank": self.rank,
                "Title": self.name,
                "Release year": self.release_year,
                "IMDB Rating": self.imdb_rating,
                "IMDB Page": self.movie_link
            }
            #print(self.movie_info)
            self.final_list.append(movie_info)
        return print(self.final_list)

def run_scrape():
    class_instance = IMDB_scrape() #create instance by assigning class with a variable
    return class_instance

if __name__ == "__main__":
    run_scrape()
else:
    print('Code not run as a script!')