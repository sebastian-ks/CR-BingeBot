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
import urllib.request
import time
import subprocess
import elem
from elem import Elements
from general import Methods
import general
from pynput.mouse import Button, Listener
import os
import mouse

#Driver class sets up Driver which opens window and loads CR
#also controls the checkups when episodes are finished and always sets the episode automatically in full-screen mode
class Driver(general.Methods):


    fullscreen = False
    savedEpisodeUrl = ""
    unclicked = True
    skipInit = False
    nextEP = ""

    def openDebug(port,saveUnder):
        cmd = 'chrome.exe -remote-debugging-port=' + str(port) + ' --user-data-dir="' + saveUnder + '"'
        subprocess.Popen('cd C:\\Program Files (x86)\\Google\\Chrome\\Application',shell=True)
        subprocess.Popen(cmd, shell=True)

    def maximize(browser,container):
        if "Folge" in browser.title or "Episode" in browser.title:
            ac = ActionChains(browser)
            ac.move_to_element(container).perform()

            dur = browser.find_elements_by_xpath("//div[@data-testid='vilos-duration']")
            max = browser.find_elements_by_xpath("//div[@data-testid='vilos-fullscreen_button']")
            if len(max) > 0 and len(dur) > 0:
                try:
                    max[0].click()
                    Driver.fullscreen = True
                    return dur[0].text
                except (ElementClickInterceptedException, StaleElementReferenceException) as egg:
                    Driver.maximize(browser,container)
            else:
                Driver.maximize(browser,container)


    def interact(browser):
        if "Folge" in browser.title or "Episode" in browser.title:
            frame = browser.find_element_by_xpath("//iframe[@id='vilos-player']")
            browser.switch_to.frame(frame)
            container = browser.find_element_by_xpath("//div[@id='vilosControlsContainer']")
            while Driver.fullscreen is not True:
                try:
                    return Driver.maximize(browser,container)
                except StaleElementReferenceException:
                    container = browser.find_element_by_xpath("//div[@id='vilosControlsContainer']")
                    return Driver.maximize(browser,container)

        browser.switch_to.default_content()

    def getInfoBox(browser):
        try:
            infobox = browser.find_element_by_xpath("//div[@id='showmedia_about_media']")
            return infobox
        except NoSuchElementException:
            Driver.getInfoBox(browser)

    def getData(browser):
        if "Folge" in browser.title or "Episode" in browser.title:
            infobox = Driver.getInfoBox(browser)#avoid nosuchelement Exception
            if infobox is not None:#func started without page loading prob so try again
                title = infobox.find_element_by_xpath(".//a[@class='text-link']").text
                h4 = infobox.find_elements_by_xpath(".//h4")
                ep = h4[1].text
                desc = browser.find_element_by_xpath("//div[@id='showmedia_about_info']")
                epName = desc.find_element_by_xpath(".//h4").text
                if title is None or ep is None or epName is None:
                    Driver.getData(browser)
                else:
                    return title,ep,epName
            else:
                Driver.getData(browser)

    def getMugs(browser,ep,title):
        if "Folge" in browser.title or "Episode" in browser.title:
            mugs = browser.find_elements_by_xpath("//img[@class='mug']")
            ep_spans = browser.find_elements_by_xpath("//span[@class='collection-carousel-overlay-top ellipsis']")
            links = browser.find_elements_by_xpath("//a[@class='link block-link block']")
            for span in ep_spans:#get mug by looking at number of episode and comparing it with episode just gotten from self.getData
                if span.text == Driver.episode(ep):
                    i = ep_spans.index(span)
                    break
            epMug = mugs[i]
            try:
                nextEp = links[i+1].get_attribute("href")
            except IndexError:
                nextEp = ""
            src = epMug.get_attribute('src')
            if "?" in title:
                title = title.replace("?", "_;")
            dir = "assets\\mugs\\"+title+"#"+Driver.season(ep)+Driver.episodeCode(ep)+".jpg"
            if not os.path.exists(dir):
                urllib.request.urlretrieve(src, dir) #downloads mug
            return nextEp

    def getEpisode(url,browser):
        if "Folge" in browser.title or "Episode" in browser.title: #don't get why this is needed, but else throws exception
            if url == "" or url is None:                           #when returning to cr_homepage after launching first ep
                return url                              #! SO IT'S NOT REDUNDANT !
            else:
                st = ""
                try:
                    area = url.split("episode-",1)[1][:4]
                except IndexError as ie:
                    print(Driver.savedEpisodeUrl)
                    print(browser.current_url)
                for i in range(len(area)):
                    try:
                        st += str(int(area[i]))
                    except ValueError as f:
                        pass
                return st


    def write_to_file(url,title,ep,epName,browser):
        if url == "" or url is None:
            return
        if "Folge" in browser.title or "Episode" in browser.title:
            if os.path.isfile("progress.txt"):
                file = open("progress.txt", "r+" )
                episodes = file.readlines()
                if episodes is not None:
                    for e in episodes:#check same series to replace
                        if Driver.getSeries(e) == title:
                            i = episodes.index(e)
                            del episodes[i]
                            episodes.append(url + "#"+title+"#"+ep+"#"+epName+ "\n")
                            file.close()
                            os.remove("progress.txt")
                            open("progress.txt", "a+" ).writelines(episodes)
                            return

                    file.write(url + "#"+title+"#"+ep+"#"+epName+ "\n") #new series entry
                else:# progress file is empty
                    file.write(url + "#"+title+"#"+ep+"#"+epName+ "\n")


    def prepareSkip(browser):
        if Methods.skipTimer:
            os.system("start pythonw skip.pyw")
        else:
            Driver.skip(browser)

    def skip(browser):
        mouse.unhook_all() #so skip doesn't trigger bc event still activated
        Driver.skipInit = False
        Driver.fullscreen = False
        browser.get(Driver.nextEP)
        Driver.unclicked = True
        Driver.nextEP = ""


    def controller(browser):
        if "Folge" in browser.title or "Episode" in browser.title: #if an episode is watched
            if (Driver.getEpisode(browser.current_url,browser) != Driver.getEpisode(Driver.savedEpisodeUrl,browser)):
                Driver.fullscreen = False
                Driver.unclicked = True
                Driver.skipInit = False
            if Driver.unclicked:
                Driver.savedEpisodeUrl = browser.current_url
                title,ep,epName = Driver.getData(browser)
                Driver.nextEP = Driver.getMugs(browser,ep,title)
                if not Methods.stne or not Driver.nextEP:
                    Driver.write_to_file(Driver.savedEpisodeUrl,title,ep,epName,browser)
                else:
                    Driver.write_to_file(Driver.nextEP,title,ep,epName,browser)
                Driver.unclicked = False
            if not Driver.fullscreen and not Driver.skipInit:
                browser.implicitly_wait(1) # loading is guaranteed to take some time so already do 5sec buffer instead of recursion in Driver.maximize()
                dur = Driver.interact(browser)
            else:
                if not Driver.skipInit and Driver.nextEP:
                    mouse.on_right_click(lambda: Driver.prepareSkip(browser))
                    Driver.skipInit = True
                if os.path.exists("temp"):
                    os.remove("temp")
                    Driver.skip(browser)

        else:
            Driver.fullscreen = False
            Driver.unclicked = True


    def setupDriver(url):
        port = 4269
        Driver.openDebug(port,"D:\\Selenium")
        options = Options()
        options.add_experimental_option("debuggerAddress","localhost:" + str(port))
        #try:
        browser = webdriver.Chrome("C:\\Users\\Zaby\\.wdm\\chromedriver\\79.0.3945.36\\win32\\chromedriver.exe",options=options)
        browser.get(url)
        browser.maximize_window()
        #except Exception as e:
        #    ctypes.windll.user32.MessageBoxW(0, "Can't reach Crunchyroll\nMake sure you are connected to the Internet" , "An Exception occured",1)
        #ChromeDriverManager().install()
        try:
            while True:
                if "Folge" in browser.title or "Episode" in browser.title:
                    Driver.controller(browser)
        except ElementNotInteractableException:
            print("loading error")
        except UnboundLocalError:
            pass
        except (NoSuchWindowException, WebDriverException) as e:
            print("browser quit because of an exception")
            print(e)
            browser.quit()
            Driver.restart() #no update because of weird bug that hides widget (no clue)
