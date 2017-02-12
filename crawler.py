import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

task = sys.argv[1]

class Linker(threading.Thread):

    def __init__(self, link, email):
        self.link = link
        #self.browser = webdriver.Chrome()
        self.browser = webdriver.PhantomJS()
        self.email = email
        threading.Thread.__init__(self)

    def extract_links(self):
        def check(string):
            interests = [" ad", "data", "lister", "poster", "listing", "advertising", "entry"]
            if any(x in string for x in interests):
                return True
            else:
                return False
        results = self.browser.find_elements_by_class_name("result-title")
        links = [str(x.get_attribute("href")) for x in results if check(x.text) == True]

        return links

    def send_via_email(self, link):    
        self.browser.get(link)
        emailBtn = self.browser.find_element_by_class_name("email-friend")
        emailBtn.click()
        time.sleep(1.5)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "S")))
        senderEmailInpt = self.browser.find_element_by_id("S")
        senderEmailInpt.send_keys(self.email)
        receiverEmailInpt = self.browser.find_element_by_id("D")
        receiverEmailInpt.send_keys(self.email)
        receiverEmailInpt.submit()
        time.sleep(.5)

    def run(self):
        self.browser.get(str(self.link) + "search/sss?query=ad+posting&sort=rel")
        listOfLinks = self.extract_links()
        for link in listOfLinks:
            self.send_via_email(link)

class Crawler():

    def __init__(self):
        #self.browser = webdriver.Chrome()
        self.browser = webdriver.PhantomJS()
        self.link = "https://www.craigslist.org/about/sites#US"
        self.email = "scraptor.ai@gmail.com"

    def login(self):
        self.browser.get("https://accounts.craigslist.org/login")
        emaiInpt = self.browser.find_element_by_id("inputEmailHandle")
        emaiInpt.send_keys("scraptor.ai@gmail.com")
        passInpt = self.browser.find_element_by_id("inputPassword")
        passInpt.send_keys("scraptor.ai@gmail.com")
        passInpt.submit()
        time.sleep(2)
        
    def getCities(self):
        self.browser.get(self.link)
        areas = self.browser.find_elements_by_css_selector(".colmask") 
        cityList = areas[0].find_elements_by_css_selector(".box li a")
        cityLinks = [el.get_attribute("href") for el in cityList]

        return cityLinks
    
    def threadingRun(self):
        for city in self.getCities():
            print "doing ", city
            Linker(city, self.email).start()

    def test(self):
        #Linker(self.getCities()[0], self.email).run()
        print self.getCities()

if task == "test":
    Crawler().test()
elif task == "crawl":
    Crawler().threadingRun()
