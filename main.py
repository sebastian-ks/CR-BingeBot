from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import ctypes
import webbrowser
import time
import subprocess
import elem
import os

#Driver class sets up Driver which opens window and loads CR
#also controls the checkups when episodes are finished and always sets the episode automatically in full-screen mode
class Driver(elem.Elements):
    fullscreen = False
    savedEpisodeUrl = ""
    unclicked = True

    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.setup()

    def openDebug(self,port,saveUnder):
        cmd = 'chrome.exe -remote-debugging-port=' + str(port) + ' --user-data-dir="' + saveUnder + '"'
        subprocess.Popen('cd C:\\Program Files (x86)\\Google\\Chrome\\Application',shell=True)
        subprocess.Popen(cmd, shell=True)

    def contHover(self,browser,container):
        if "Folge" in browser.title or "Episode" in browser.title:
            ac = ActionChains(browser)
            ac.move_to_element(container).perform()
            elem = browser.find_elements_by_xpath("//div[@data-testid='vilos-fullscreen_button']")
            if len(elem) > 0:
                try:
                    elem[0].click()
                    self.fullscreen = True
                except (ElementClickInterceptedException, StaleElementReferenceException) as egg:
                    self.contHover(browser,container)
            else:
                self.contHover(browser,container)


    def maximize(self,browser):
        if "Folge" in browser.title or "Episode" in browser.title:
            frame = browser.find_element_by_xpath("//iframe[@id='vilos-player']")
            browser.switch_to.frame(frame)
            container = browser.find_element_by_xpath("//div[@id='vilosControlsContainer']")
            while self.fullscreen is not True:
                try:
                    self.contHover(browser,container)
                except StaleElementReferenceException:
                    container = browser.find_element_by_xpath("//div[@id='vilosControlsContainer']")
                    self.conHover(browser,container)

        browser.switch_to.default_content()


    def getSeries(self,url):
        if url == "" or url is None:
            return url
        else:
            st = url.split("https://www.crunchyroll.com/",1)[1]
            st = st.split("/episode")[0]
            if "de" in st:
                st = st.split("/")[1]
            return st

    def getEpisode(self,url,browser):
        if "Folge" in browser.title or "Episode" in browser.title: #don't get why this is needed, but else throws exception
            if url == "" or url is None:                           #when returning to cr_homepage after launching first ep
                return url                              #! SO IT'S NOT REDUNDANT !
            else:
                st = ""
                try:
                    area = url.split("episode-",1)[1][:4]
                except IndexError as ie:
                    print("das ist die url:" + url)
                for i in range(len(area)):
                    try:
                        st += str(int(area[i]))
                    except ValueError as f:
                        pass
                return st


    def getEpisodeID(self,url):
        first = 0
        if url == "" or url is None:
            return url
        else:
            st = url[-7:]
            for letter in st:
                try:
                    first = int(letter)
                    first = st.index(letter)
                    break
                except:
                    pass
            newst = st[first:]
            return int(newst)

    def write_to_file(self,url,browser):
        if url == "" or url is None:
            return
        if "Folge" in browser.title or "Episode" in browser.title:
            if os.path.isfile("progress.txt"):
                file = open("progress.txt", "r+")
                episodes = file.readlines()
                if episodes is not None:
                    for e in episodes:#check for sequel episode
                        if self.getSeries(e) == self.getSeries(url):
                            if self.getEpisodeID(e) < self.getEpisodeID(url): # ID to also detect new seasons
                                del episodes[episodes.index(e)]
                                episodes.append(url + "\n")
                                file.close()
                                os.remove("progress.txt")
                                open("progress.txt", "a+").writelines(episodes)
                                return
                            else:
                                return
                    file.write(url + "\n") #new series entry
                else:# progress file is empty
                    file.write(url + "\n")
            else:#progress file does not exist
                file = open("progress.txt", "a+")
                file.write(url + "\n")


    def controller(self,browser):
        if "Folge" in browser.title or "Episode" in browser.title: #if an episode is watched
            if (self.getEpisode(browser.current_url,browser) != self.getEpisode(self.savedEpisodeUrl,browser)):
                self.fullscreen = False
                self.unclicked = True
            if self.unclicked:
                self.savedEpisodeUrl = browser.current_url #<-- update which episode is played currently
                self.write_to_file(self.savedEpisodeUrl,browser)
                self.unclicked = False
            if not self.fullscreen:
                browser.implicitly_wait(1) # loading is guaranteed to take some time so already do 5sec buffer instead of recursion in self.maximize()
                self.maximize(browser)
        else:
            self.fullscreen = False
            self.unclicked = True


    def setupDriver(self):
        port = 4269
        self.openDebug(port,"D:\\Selenium")
        options = Options()
        options.add_experimental_option("debuggerAddress","localhost:" + str(port))
        try:
            browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            browser.get(elem.destination)
            browser.maximize_window()
        except:
            ctypes.windll.user32.MessageBoxW(0, "Can't reach Crunchyroll\nMake sure you are connected to the Internet" , "An Exception occured",1)

        try:
            while True:
                self.controller(browser)
        except ElementNotInteractableException:
            print("loading error")
        except UnboundLocalError:
            pass
        except (NoSuchWindowException, WebDriverException) as e:
            print("browser quit because of an exception")
            browser.quit()
