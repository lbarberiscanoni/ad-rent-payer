import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import subprocess
from random import randint
from gmailModule import Gmail

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
        #self.browser.get("https://post.craigslist.org/k/NGrYPL_05hGDQzWBu9LzZA/ZpupS?s=type")
        self.browser.get("https://sfbay.craigslist.org")
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
        laborGig = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(6) label span:nth-of-type(1) input")
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
            newZipCode = self.browser.find_element_by_id("postal_code")
            newZipCode.clear()
            newZipCode.send_keys("94110")
            searchZip = self.browser.find_element_by_id("search_button")
            searchZip.click()
            time.sleep(1)
            continueBtn.click()
        except:
            print "no alert"
        time.sleep(2)
        try:
            doneWithImagesBtn = self.browser.find_element_by_css_selector(".done.bigbutton")
            doneWithImagesBtn.click()
            time.sleep(1)
        except:
            print "no images requested"
        publishBtn = self.browser.find_element_by_css_selector("#publish_top .button")
        publishBtn.submit()

    def checkEmailForLink(self):
        g = Gmail()
        g.login("scraptor.ai@gmail.com", "pay4rent")
        unreadEmails = g.inbox().mail(unread = True)
        link = False
        for email in unreadEmails:
            email.fetch()
            email.read()
            if "POST/EDIT/DELETE:" in str(email.subject):
                link = [x for x in str(email.body).split("\n") if "https" in x][0]

        return link

    def publish(self):
        link = self.checkEmailForLink()
        self.browser.get(link)
        acceptBtn = self.browser.find_element_by_css_selector(".previewButtons form button")
        acceptBtn.click()
        postLink = self.browser.find_element_by_css_selector(".body .ul li a").get_attribute("href")
        return postLink

    def run(self):
        self.job_flow()
        self.post()
        time.sleep(5)
        link = self.publish()
        print link


def main():
    for i in range(0, 10):
        status = 0
        while status == 0:
            try:
                Poster().run()
                status = 1
            except:
                print "trying again"
        time.sleep(300) 

main()
