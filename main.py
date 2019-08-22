from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import webbrowser
import time
import subprocess

#Driver class sets up Driver which opens window and loads CR
#also controls the checkups when episodes are finished and always sets the episode automatically in full-screen mode
class Driver():
    fullscreen = False
    savedEpisodeUrl = ""
    unclicked = True
    durationTime = False

    def openDebug(self,port,saveUnder):
        cmd = 'chrome.exe -remote-debugging-port=' + str(port) + ' --user-data-dir="' + saveUnder + '"'
        subprocess.Popen('cd C:\\Program Files (x86)\\Google\\Chrome\\Application',shell=True)
        subprocess.Popen(cmd, shell=True)


    def maximize(self,browser):
        frames= browser.find_elements_by_tag_name('iframe')
        for index in range(len(frames)):
            browser.switch_to.default_content()
            frame = browser.find_elements_by_tag_name('iframe')[index]
            browser.switch_to.frame(frame)
            elem = browser.find_element_by_class_name('vjs-fullscreen-control')
            if elem is not None:
                try:
                    elem.click()
                    self.fullscreen = True
                    break
                except ElementNotInteractableException: #trying to click while still loading throws exception #if video is loading to long wait 5 sec and than try process again
                    self.maximize(browser)
                    break

        browser.switch_to.default_content()

    #def startedEpisode(self,durTime,secs,browser):
    #    skipTriggerTime = 90 #Trigger skip with 90 == skip request 1:30 bevore episode ends
    #    while secs is not durTime-skipTriggerTime:
    #        time.sleep(1)
    #        secs += 1
    #        if self.paused(browser):
    #            break
    #    if self.paused(browser):
    #        print("paused")

    def zeroint(self,durTime,part):#part int : 0 for min , 1 for seconds üart of time display
        sp = durTime.split(":")[part]
        if(int(sp[0]) is 0):
            time = int(sp[1])
        else:
            time = int(sp)
        return time


    def sec(self,durTime):
        min = self.zeroint(durTime,0)
        sec = self.zeroint(durTime,1)
        return min*60+sec

    def getEpisode(self,url):
        if url == "" or url is None:
            return url
        else:
            st = ""
            area = url.split("episode-",1)[1][:4]
            for i in range(len(area)):
                try:
                    st += str(int(area[i]))
                except ValueError as f:
                    pass
            return st


    def controller(self,browser):
        if "Folge" in browser.title or "Episode" in browser.title: #if an episode is watched
            if (self.getEpisode(browser.current_url) != self.getEpisode(self.savedEpisodeUrl)):
                print("neue folge")
                self.fullscreen = False
                self.unclicked = True
                self.durationTime = False
            if self.unclicked:
                self.savedEpisodeUrl = browser.current_url #<-- update which episode is played currently
                self.unclicked = False
            if not self.fullscreen:
                browser.implicitly_wait(1) # loading is guaranteed to take some time so already do 5sec buffer instead of recursion in self.maximize()
                self.maximize(browser)
            #else:
            #    self.startedEpisode(sec(self.durTime),0,browser)
        else:
            self.fullscreen = False
            self.unclicked = True
            self.durationTime = False



    def setupDriver(self):
        port = 4269
        self.openDebug(port,"D:\\Selenium")
        options = Options()
        options.add_experimental_option("debuggerAddress","localhost:" + str(port))
        try:
            browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            browser.get("https://www.crunchyroll.com/")
            browser.maximize_window()
        except:
            print("no internet")

        try:
            while True:
                self.controller(browser)
        except ElementNotInteractableException:
            print("loading error")
        except UnboundLocalError:
            print("no internet")
        except (NoSuchWindowException, WebDriverException) as e:
            print("browser quit because of an exception")
            browser.quit()



if __name__ == '__main__':
    Driver.setupDriver(Driver())
