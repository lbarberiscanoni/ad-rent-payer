import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import subprocess
from random import randint, uniform
from gmailModule import Gmail
from pprint import pprint

client = sys.argv[1]

class Poster():

    def __init__(self, ob, browser):
        self.email = ob["email"]
        self.client = ob["client"]
        self.password = ob["password"]
        self.browser = browser
        self.phone_num = ob["phone_num"]
        self.name = ob["name"]
        title_options = ob["title_options"]
        self.title = title_options[randint(0, len(title_options) - 1)]
        self.body = ob["body"]
        self.payment = ob["payment"]
        self.state = ""
        self.zipCodes = {"ak": "99824", "al": "36103", "ar": "72002", "az": "85001", "ca": "94110", "co": "80241", "ct": "061", "de": "19901", "fl": "32300", "ga": "30060", "hi": "96801", "ia": "50340", "id": "83701", "il": "62701", "in": "46211", "ks": "66622", "ky": "40601", "la": "70801", "ma": "02203", "md": "21409", "me": "02100", "mi": "48980", "mn": "55175", "mo": "65111", "ms": "39299", "mt": "59604", "nc": "27601", "nd": "58507", "ne": "68512", "nh": "14200", "nj": "08625", "nm": "87599", "nv": "89721", "ny": "12220", "oh": "43251", "ok": "73167", "or": "97305", "pa": "17177", "ri": "02918", "sc": "29223", "sd": "57501", "tn": "37250", "tx": "78708", "ut": "84141", "va": "23255", "vt": "05609", "wa": "98599", "wi": "53702", "wv": "25317", "wy": "82002"}

    def send_keys(self, ob, string):
        try:
            ob.clear()
        except Exception as e:
            print e
        for letter in string:
            ob.send_keys(letter)
            time.sleep(uniform(0.1, 0.3))

    def login(self):
        self.browser.get("https://accounts.craigslist.org/login")
        emailInpt = self.browser.find_element_by_id("inputEmailHandle")
        self.send_keys(emailInpt, self.email)
        passInpt = self.browser.find_element_by_id("inputPassword")
        self.send_keys(passInpt, self.password)
        passInpt.submit()

    def submit(self):
        submitBtn = self.browser.find_element_by_class_name("pickbutton")
        submitBtn.submit()

    def job_flow(self):
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
        try:
            numOfRegions = int(len(self.browser.find_elements_by_css_selector(".selection-list li")))
            regionInpt = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(" + str(randint(1, numOfRegions - 1)) + ") label input")
            regionInpt.click()
            #self.submit()
        except:
            print "no need to speciy the region"
        time.sleep(1)
        try:
            numOfCities = int(len(self.browser.find_elements_by_css_selector(".selection-list li")))
            cityInpt = self.browser.find_element_by_css_selector(".selection-list li:nth-of-type(" + str(randint(1, numOfCities - 1)) + ") label span:nth-of-type(1) input")
            cityInpt.click()
        except:
            print "no city to select"
        time.sleep(1)

    def zipCode(self, city):
        try:
            self.browser.get("https://www.zip-codes.com/search.asp?fld-address=&fld-city2=" + city + "&fld-state2=" + self.state)
            zipCode = self.browser.find_element_by_css_selector("tr td.a a")
            zipCode = str(zipCode.text)
        except:
            zipCode = self.zipCodes[self.state]
        
        return zipCode

    def getCityName(self):
        try:
            cityName = self.browser.find_element_by_tag_name("b")
            cityName = str(cityName.text).replace(" ", "+").replace("(", "").replace(")", "")
        except:
            cityName = str(self.browser.current_url).split(".craigslist")[0].split("//")[1]

        return cityName

    def post(self):
        cityName = self.getCityName()
        zipCode = self.zipCode(cityName)
        self.browser.back()
        emailInpt = self.browser.find_element_by_id("FromEMail")
        self.send_keys(emailInpt, self.email)
        emailInpt = self.browser.find_element_by_id("ConfirmEMail")
        self.send_keys(emailInpt, self.email)
        contactTextOkInpt = self.browser.find_element_by_id("contact_text_ok")
        contactTextOkInpt.click()
        phoneInpt = self.browser.find_element_by_id("contact_phone")
        self.send_keys(phoneInpt, self.phone_num)
        contactInpt = self.browser.find_element_by_id("contact_name")
        self.send_keys(contactInpt, self.name)
        titleInpt = self.browser.find_element_by_id("PostingTitle")
        self.send_keys(titleInpt, self.title)
        zipInpt = self.browser.find_element_by_id("postal_code")
        self.send_keys(zipInpt, zipCode)
        bodyInpt = self.browser.find_element_by_id("PostingBody")
        self.send_keys(bodyInpt, self.body)
        payRdio = self.browser.find_element_by_id("pay_label")
        payRdio.click()
        payInpt = self.browser.find_element_by_id("remuneration")
        self.send_keys(payInpt, self.payment)
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
            self.send_keys(newZipCode, self.zipCodes[self.state])
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
        g.login(self.email, self.password)
        unreadEmails = g.inbox().mail(unread = True)
        link = False
        for email in unreadEmails:
            email.fetch()
            if "POST/EDIT/DELETE:" in str(email.subject):
                email.read()
                link = [x for x in str(email.body).split("\n") if "https" in x][0]

        return link

    def publish(self):
        link = self.checkEmailForLink()
        self.browser.get(link)
        acceptBtn = self.browser.find_element_by_css_selector(".previewButtons form button")
        acceptBtn.click()
        postLink = self.browser.find_element_by_css_selector(".body .ul li a").get_attribute("href")
        return postLink

    def getCities(self):
        self.browser.get("https://www.craigslist.org/about/sites#US")
        areas = self.browser.find_elements_by_css_selector(".colmask") 
        cityList = areas[0].find_elements_by_css_selector(".box li a")
        cityLinks = [el.get_attribute("href") for el in cityList]

        return cityLinks

    def getState(self, link):
        self.browser.get(str(link))
        state = self.browser.find_element_by_css_selector("#topban .regular-area .area").text.split(",")[1].strip()

        return state

    def confimationEmail(self, link):
        orderUpdate = "python gmailText.py -u " + self.email + " -p " + self.password + " -t " + self.client + " -s 'Latest Ad'" + " -b '" + str(link) + "'"
        subprocess.call(orderUpdate, shell=True)
        print "successfully sent the email"

    def run(self):
        cityLinks = self.getCities()
        attemptStatus = 0
        location = ""
        while attemptStatus < 1:
            try:
                url = str(cityLinks[randint(0, len(cityLinks) - 1)])
                self.browser.get(url)
                location = self.getState(url)
                attemptStatus += 1
            except:
                print "location not available"
        self.state = location.lower()
        self.job_flow()
        self.post()
        time.sleep(5)
        link = self.publish()
        print link
        self.confimationEmail(str(link))

class Selector():

    def __init__(self, client):
        self.client = client

    def loadSpecs(self):
        f = open("specs.txt", "r")
        txt = f.read()
        raw_data = json.loads(txt.replace("'", "\""))
        f.close()
        
        self.specs = raw_data[self.client]

    def run(self):
        self.loadSpecs()
        for i in range(0, 10):
            print "doing #", i
            status = 0
            while status == 0:
                if sys.platform == "darwin":
                    browser = webdriver.Chrome()
                else:
                    browser = webdriver.PhantomJS()
                try:
                    Poster(self.specs, browser).run()
                    status = 1
                    browser.close()
                except Exception as e:
                    print e
                    browser.close()
                    print "trying again"
            time.sleep((35 + randint(5, 15)) * 60)

Selector(client).run()
