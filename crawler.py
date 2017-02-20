import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import subprocess

task = sys.argv[1]
content = sys.argv[2]

titles = []
class Linker():

    def __init__(self, browser, link, email):
        self.link = link
        self.browser = browser
        self.email = email
        content_options = {
                "ads": [" ad", "survey", "data", "lister", "poster", "posting", "listing", " post ", "advertising", "entry", "ebay"],
                "code": ["programming", "developer", "app", "website", "coder", "code", "software", "twitter", "software", "web design", "e-commerce"]
        }
        self.interests = content_options[content]

    def extract_links(self):
        def check(string):
            if any(x in string.lower() for x in self.interests):
                if string.lower().strip() in titles:
                    return False
                else:
                    titles.append(string.lower().strip())
                    return True
            else:
                return False
        results = self.browser.find_elements_by_class_name("result-title")
        obs = [{"title": x.text, "link": x.get_attribute("href")} for x in results if check(x.text) == True]

        return obs


    def send_via_email(self, title, link):    
        orderUpdate = "python gmailText.py -u " + self.email + " -p pay4rent -t " + self.email + " -s '" + str(title).replace("\"", "").replace("'", "") + "' -b '" + str(link) + "'"
        subprocess.call(orderUpdate, shell=True)

    def getState(self):
        self.browser.get(str(self.link))
        state = self.browser.find_element_by_css_selector("#topban .regular-area .area").text.split(",")[1].strip()

        return state

    def run(self):
        stateCode = self.getState()
        self.browser.get(str(self.link) + "search/ggg?query=ad+poster&sort=rel")
        applicableAds = self.extract_links()
        for el in applicableAds:
            self.send_via_email(el["title"], el["link"])

class Crawler():

    def __init__(self):
        if sys.platform == "darwin":
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.PhantomJS()
        self.link = "https://www.craigslist.org/about/sites#US"
        if content == "ads":
            self.email = "scraptor.ai@gmail.com"
        elif content == "code":
            self.email = "dreamage.ai@gmail.com"

    def login(self):
        self.browser.get("https://accounts.craigslist.org/login")
        emaiInpt = self.browser.find_element_by_id("inputEmailHandle")
        emaiInpt.send_keys(self.email)
        passInpt = self.browser.find_element_by_id("inputPassword")
        passInpt.send_keys(self.email)
        passInpt.submit()
        time.sleep(2)
        
    def getCities(self):
        self.browser.get(self.link)
        areas = self.browser.find_elements_by_css_selector(".colmask") 
        cityList = areas[0].find_elements_by_css_selector(".box li a")
        cityLinks = [el.get_attribute("href") for el in cityList]

        return cityLinks
    
    def threadingRun(self):
        i = 0
        for city in self.getCities():
            print "doing #", i, city
            #Linker(city, self.email).start()
            try:
                Linker(self.browser, city, self.email).run()
            except Exception as e:
                print e
            i += 1

    def test(self):
        #Linker(self.getCities()[0], self.email).run()
        print self.getCities()

if task == "test":
    Crawler().test()
elif task == "crawl":
    Crawler().threadingRun()
