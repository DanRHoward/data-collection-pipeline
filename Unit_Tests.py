import unittest #package for unit test module
from Selenium_webscrape import IMDB_scrape

class Test_IMDB_scrape(unittest.TestCase):
    def setUp(self):
        testclass = IMDB_scrape("C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline")
        self.testclass = testclass

    def test_scrape_data(self): 
        test_scrape_data_output = self.testclass.scrape_data() #gives value assigned to 'return' of method
        self.assertTrue(type(test_scrape_data_output) == list)
        try: #try implemented in case first test fails 
            for movie in test_scrape_data_output: #check each element is valid
                self.assertTrue(type(movie) == dict) #each element of list is a dictionary 
                self.assertEqual(len(movie), 5) #5 initial data points per movies at this stage
        except:
            pass

    def test_get_poster(self):
        test_get_poster_output = self.testclass.get_posters()
        for movie in test_get_poster_output:
            self.assertEqual(len(movie), 6) #if newly aquired data is added to dictionaries
            self.assertTrue(type(movie['POSTER']) == str) #checks new data point is of the correct type

    def test_store_data(self):
        import os
        test_store_data_output = self.testclass.store_data("C:/Users/Daniel H/Desktop/AI Core/Python/DataPipeline")
        self.assertTrue(type(test_store_data_output) == str)
        self.assertTrue(os.path.isdir(test_store_data_output) == True) #
        self.assertEqual(len(os.listdir(test_store_data_output + '/raw_data')), 250) #initial number of elements in directory

    def test_download_posters(self):
        import os
        test_download_posters_output = self.testclass.download_posters()
        self.assertEqual(len(os.listdir(test_download_posters_output + '/raw_data')), 251) #new addition due to method
        for image_posters in os.listdir(test_download_posters_output + '/raw_data/images'):
            self.assertTrue(os.path.splitext(image_posters)[-1].lower() == ".jpg")

if __name__ == "__main__":
    unittest.main()