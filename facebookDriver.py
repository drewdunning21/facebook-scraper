import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from retry import retry
import pickle
from bs4 import BeautifulSoup

class FacebookDriver:
    def __init__(self,email,pw):
        self.email = email
        self.pw = pw
        self.driver = self.makeDriver()

    def makeDriver(self):
        driver = webdriver.Chrome(executable_path = '/Users/andrewdunning/Documents/facebook-scraper/chromedriver')
        return driver

    def login(self):
        '''
        logs into facebook
        uses the email and pw passed into the class upon creation
        '''
        # navigates to fb if not already there
        self.driver.get('https://facebook.com')
        self.loadCookies()
        if not self.checkLogin():
            emailElem = self.driver.find_element_by_id('email')
            print('Typing email')
            self.type(emailElem, self.email)
            print('Typing password')
            pwElem = self.driver.find_element_by_id('pass')
            self.type(pwElem, self.pw)
            pwElem.send_keys(Keys.ENTER)
            self.awaitLogin()
            pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))

    def loadCookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get('https://facebook.com')

    def checkLogin(self):
        if 'timeline' in self.driver.page_source:
            print('Logged in')
            return True
        print('Not logged in')
        return False

    def awaitLogin(self):
        while 'timeline' not in self.driver.page_source:
            sleep(.1)
        print('logged in')
        return

    def getInterests(self,link):
        self.driver.get(link)
        pages = {
                'movies':'movies',
                'music':'music',
                'tv':'TV Shows',
                'games':'Apps and Games',
                'sports':'Sports',
                'map':'places',
                'books':'Books',
                'events':'Events',
                'sports':'Sports'
                }
        pageUrls = pages.keys()
        pageNames = pages.values()
        print(pageUrls)
        print(pageNames)
        for key, value in pages.items():
            self.getInfo(link,key,value)
            print('\n')

    def getInfo(self, link,page,name):
        print('Getting ' + name)
        self.driver.get(link + '/' + page)
        sleep(3)
        info = []
        parent = self.getElem('j83agx80 l9j0dhe7 k4urcfbm','@class')
        html = parent.get_attribute('outerHTML')
        if 'no ' + name.lower() + ' to show' in html:
            print('No ' + name)
            return info
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('span', class_=['oi732d6d', 'ik7dh3pa', 'd2edcug0', 'qv66sw1b', 'c1et5uql', 'a8c37x1j', 'muag1w35', 'enqfppq2', 'a5q79mjw', 'g1cxx5fr', 'lrazzd5p', 'oo9gr5id'])
        for i in range(0,len(items),2):
            text = items[i].text.lower()
            if 'no' not in text and 'to show' not in text:
                print(i.text)
        return info
         

    @retry()
    def type(self, element, words):
        '''
        - a function that types text into an element text box
        - element is an element selenium object
        - words is text to be typed into the box
        '''
        element.send_keys(words)
        # checks if it was typed incorrectly and deletes if so
        if element.text != words:
            element.send_keys(u'\ue009' + u'\ue003')

    @retry()
    def getElem(self,element,selType):
        sleep(.2)
        xpath = '//*[' + selType + '="' + element + '"]'
        element = self.driver.find_element(By.XPATH, xpath)
        return element
