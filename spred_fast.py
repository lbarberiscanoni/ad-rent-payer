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
        self.phone_num = "5712103649"
        self.name = "David"
        self.title = "NEED A CRAIGSLIST POSTER"
        self.body = "Make $450 cash weekly by posting on craigslist\n\nContact Mr David (571) 210-3649 for more info, text only."
        self.payment = "$450 weekly"

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
        self.browser.get("https://houston.craigslist.org")
        postToClassifiedBtn = self.browser.find_element_by_id("post")
        postToClassifiedBtn.click()
        time.sleep(1)
        time.sleep(2)
        gigRdio = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(2) label span:nth-of-type(1) input")
        gigRdio.click()
        self.submit()
        time.sleep(1)
        self.submit()
        time.sleep(1)
        laborGig = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(4) label span:nth-of-type(1) input")
        laborGig.click()
        time.sleep(1)

    def zipCode(self, city):
        try:
            self.browser.get("https://www.zip-codes.com/search.asp?fld-address=&fld-city2=" + city + "&fld-state2=TX")
            zipCode = self.browser.find_element_by_css_selector("tr td.a a")
            zipCode = str(zipCode.text)
        except:
            zipCode = "77010"
        
        return zipCode

    def post(self):
        cityName = "Houston"
        zipCode = self.zipCode(cityName)
        self.browser.back()
        emailInpt = self.browser.find_element_by_id("FromEMail")
        emailInpt.clear()
        emailInpt.send_keys(self.email)
        emailInpt = self.browser.find_element_by_id("ConfirmEMail")
        emailInpt.clear()
        emailInpt.send_keys(self.email)
        contactTextOkInpt = self.browser.find_element_by_id("contact_text_ok")
        contactTextOkInpt.click()
        phoneInpt = self.browser.find_element_by_id("contact_phone")
        phoneInpt.clear()
        phoneInpt.send_keys(self.phone_num)
        contactInpt = self.browser.find_element_by_id("contact_name")
        contactInpt.clear()
        contactInpt.send_keys(self.name)
        titleInpt = self.browser.find_element_by_id("PostingTitle")
        titleInpt.clear()
        titleInpt.send_keys(self.title)
        zipInpt = self.browser.find_element_by_id("postal_code")
        zipInpt.clear()
        zipInpt.send_keys(zipCode)
        bodyInpt = self.browser.find_element_by_id("PostingBody")
        bodyInpt.clear()
        bodyInpt.send_keys(self.body)
        payRdio = self.browser.find_element_by_id("pay_label")
        payRdio.click()
        payInpt = self.browser.find_element_by_id("remuneration")
        payInpt.clear()
        payInpt.send_keys(self.payment)
        payInpt.submit()
        time.sleep(1)
        pinBtn = self.browser.find_element_by_id("search_button")
        pinBtn.click()
        continueBtn = self.browser.find_element_by_css_selector(".continue.bigbutton")
        continueBtn.click()
        time.sleep(1)
        try:
            alert = self.browser.switch_to_alert()
            alert.accept()
        except:
            print "no alert"
        try:
            doneWithImagesBtn = self.browser.find_element_by_css_selector(".done.bigbutton")
            doneWithImagesBtn.click()
            time.sleep(1)
        except:
            print "no images requested"
        publishBtn = self.browser.find_element_by_css_selector("#publish_top .button")
        publishBtn.submit()

    def run(self):
        self.job_flow()
        self.post()
        time.sleep(5)


try:
    Poster().run()
except:
    Poster().run()
