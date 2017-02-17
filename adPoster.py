import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import subprocess
from random import randint

#task = sys.argv[1]

class Poster():

    def __init__(self):
        self.email = "scraptor.ai@gmail.com"
        self.password = "pay4rent"
        self.browser = webdriver.Chrome()
        self.phone_num = "3343772470"
        self.name = "Jesse"
        self.title = "Make $500 Weekly"
        self.body = "HELLO, Would you allow Bud Wiser to put a small sticker on your CAR, TRUCK, OR MOTORCYCLE, For Bud Company Promo Advertising and received $500 every week?! The program will last for 3 months...\n\n if you are interested please text (334) 377-2470  for more details \n\n Ask for Jesse"
        self.payment = "$500 weekly"

    def login(self):
        self.browser.get("https://accounts.craigslist.org/login")
        emailInpt = self.browser.find_element_by_id("inputEmailHandle")
        emailInpt.send_keys(self.email)
        passInpt = self.browser.find_element_by_id("inputPassword")
        passInpt.send_keys(self.password)
        passInpt.submit()

    def submit(self):
        submitBtn = self.browser.find_element_by_class_name("pickbutton")
        submitBtn.submit()

    def job_flow(self):
        self.browser.get("https://post.craigslist.org/k/NGrYPL_05hGDQzWBu9LzZA/ZpupS?s=type")
        time.sleep(2)
        gigRdio = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(2) label span:nth-of-type(1) input")
        gigRdio.click()
        self.submit()
        time.sleep(1)
        self.submit()
        time.sleep(1)
        laborGig = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(5) label span:nth-of-type(1) input")
        laborGig.click()
        #self.submit()
        time.sleep(1)
        numOfRegions = int(len(self.browser.find_elements_by_css_selector(".selection-list li")))
        regionInpt = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(" + str(randint(1, numOfRegions - 1)) + ") label input")
        regionInpt.click()
        #self.submit()
        time.sleep(1)
        numOfCities = int(len(self.browser.find_elements_by_css_selector(".selection-list li")))
        cityInpt = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(" + str(randint(1, numOfCities - 1)) + ") label span:nth-of-type(1) input")
        cityInpt.click()

    def zipCode(self, city):
        try:
            self.browser.get("https://www.zip-codes.com/search.asp?fld-address=&fld-city2=" + city + "&fld-state2=CA")
            zipCode = self.browser.find_element_by_css_selector("tr td.a a")
            zipCode = str(zipCode.text)
        except:
            zipCode = "94101"
        
        return zipCode

    def post(self):
        cityName = self.browser.find_element_by_tag_name("b")
        cityName = str(cityName.text).replace(" ", "+").replace("(", "").replace(")", "")
        zipCode = self.zipCode(cityName)
        self.browser.back()
        emailInpt = self.browser.find_element_by_id("FromEMail")
        emailInpt.send_keys(self.email)
        emailInpt = self.browser.find_element_by_id("ConfirmEMail")
        emailInpt.send_keys(self.email)
        contactTextOkInpt = self.browser.find_element_by_id("contact_text_ok")
        contactTextOkInpt.click()
        phoneInpt = self.browser.find_element_by_id("contact_phone")
        phoneInpt.send_keys(self.phone_num)
        contactInpt = self.browser.find_element_by_id("contact_name")
        contactInpt.send_keys(self.name)
        titleInpt = self.browser.find_element_by_id("PostingTitle")
        titleInpt.send_keys(self.title)
        zipInpt = self.browser.find_element_by_id("postal_code")
        zipInpt.send_keys(zipCode)
        bodyInpt = self.browser.find_element_by_id("PostingBody")
        bodyInpt.send_keys(self.body)
        payRdio = self.browser.find_element_by_id("pay_label")
        payRdio.click()
        payInpt = self.browser.find_element_by_id("remuneration")
        payInpt.send_keys(self.payment)
        self.submit()

    def run(self):
        #self.login()
        self.job_flow()
        self.post()
        time.sleep(15)

Poster().run()

