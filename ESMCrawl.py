#import webdriver from selenium
from selenium import webdriver

#import Select which may be useful later on
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
#fpdf module used for creating and managing the pdf with the result of each test
from fpdf import FPDF
#import time and os module
import time
import os
#Get Path of geckodriver

path = os.path.abspath("geckodriver.exe")
print(path)
#ESMCrawl class (automation running class) used to start up the automation
class ESMCrawl:

    #init of the class, contains predefined variables which will be used throughout the class
    def __init__(self,username,password,urls):
        #url variable
        self.urls = urls
        #options variable for defining any specifications for the drvier
        self.options = webdriver.FirefoxOptions()
        self.flflag = False
        #counter for screenshots
        self.counter1 = 0
        #counter for iterating through different folders
        self.counter = 0
        #timeoutcounter to avoid infinite loops
        self.timeoutcount =  0
        #Dicitionary containing languages which we will log in using
        self.languages = {"English US": False, "中文 (台灣) (Traditional Chinese)": False, "Deutsch (German)": False,
        "日本語 (Japanese)":False, "Français (French)": False, "Español (Spanish)": False, "Português (Brazil)": False,
        "한국어 (Korean)": False, "中文 (简体) (Simplified Chinese)": False }
        #List containing the names of each screenshot function
        self.Folders = ["en_US", "zh_TW","de_DE","ja_JP","fr_FR","es_ES","pt_BR","ko_KR","zh_CN"]
        #username for logging in
        self.username = username
        #variable for the current language
        self.currlang = ""
        #instance of pdf created
        self.pdf = FPDF()

        #password for logging in
        self.password = password
        #command for creating the screenshots directory
        os.mkdir("Screenshots")
        #logon function which opens logon page
        #for loop which iterates through languages to login
        for language in self.languages:
            #checks that a language has not been tested
            if self.languages[language] == False:

                #variable/flag to stop pdf from storing every test of opening tabs
                self.opentabrecorded = False
                #variable/flag to stop pdf from storing every test of opening menu
                self.openmenurecorded = False
                #variable/flag to stop pdf from storing every test of opening default view tab
                self.opendefaultrecorded = False
                #variable/flag to stop pdf from storing every test of opening new view
                self.openviewrecorded = False
                self.pdf.add_page(orientation = 'P')
                #sets pdf font
                self.pdf.set_font('Arial','B',16)
                #adding a new cell, the first two values are the size of the cell, the third is the text, fourth is bordered or not and fifth is if the next cell will start on a new line
                self.pdf.cell(40,20,self.Folders[self.counter],0,1,"C")
                #adds a space after the cell
                self.pdf.ln(20)
                self.pdf.cell(40,20,"Test Name",1,0,"C")
                self.pdf.cell(40,20,"Error Message",1,0,"C")
                self.pdf.cell(40,20,"Times Failed",1,0,"C")
                self.pdf.cell(40,20,"Result",1,1,"C")
                self.pdf.set_font('Arial','B',8)
                #creates the web driver instance
                self.driver =  webdriver.Firefox(executable_path=str(path),options = self.options)
                self.Logon()
                #makes folder for each languages screenshot
                os.mkdir("Screenshots//%s" %(self.Folders[self.counter]))
                self.languages[language]= True
                #current language variable
                self.currlang = self.Folders[self.counter]
                self.counter += 1

                #langchange function
                self.langchange(language,0,"None","Pass",False)
                self.pdf.ln(2)
                #cells which contain screenshot count
                self.pdf.cell(40,20,"Total Screenshots",1,0,"C")
                self.pdf.cell(40,20,str(self.counter1),1,1,"C")
                self.counter1 = 0
                #closes driver after each language
                self.driver.close()
    #langchange function which deals with input username and password and selecting the current language
        self.pdf.output('test.pdf','F')
        #self.addTab ,self.menuClicks
    #Function which iterates through each function in the automation and calls them
    def logoff(self,language):
        #list containing the function that will be called in order
        y = [self.physcialdisplay,self.dropdownref,self.threedots,self.advsearch,self.notificationOpen,self.datastreamingbus,self.menuClicks,self.addTab,self.FLFeatures,self.ddownOpen,self.LogOut]
        for i in y:
            try:
                time.sleep(1)
                self.timeoutcount = 0
                i(0,"None","Pass",False)
            except:
                pass 
    #function which opens physical display
    def physcialdisplay(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            physdis = self.driver.find_element_by_xpath("//span[@class = 'siem-header-text hidden-xs hidden-sm hidden-md']")
            physdis.click()
            time.sleep(3)
            self.SS("Phsyical Display")
            devicedropdown = self.driver.find_element_by_xpath("//button[@class = 'uc-select-header uc-btn-clear uc-collapsed']")
            devicedropdown.click()
            time.sleep(2)
            self.SS("Device Dropdown")
            physdis.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            print("physical display error %s", error)
            count += 1
            time.sleep(5)
            return self.physcialdisplay(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Physical Display",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded

    #function which opens drop down for the refresh tab
    def dropdownref(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(10)
            refddown = self.driver.find_element_by_xpath("//i[@class='i-down']")
            refddown.click()
            time.sleep(10)
            self.SS("Refresh Dropdown")
            refddown.click()
            currday = self.driver.find_element_by_xpath("//span[@class = 'ui-core-drop-down-toggle-text-span']")
            time.sleep(2)
            currday.click()
            time.sleep(2)
            self.SS("Current Day Dropdown")
            currday.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            print("refresh drop down error %s", error)
            time.sleep(5)
            count +=1
            return self.dropdownref(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Refresh Drop Down",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function which opens three dot drop down
    def threedots(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            threedot = self.driver.find_element_by_xpath("//button[@class = 'uc-btn-clear uc-btn-tertiary uc-icon i-extra-menu siem-widget-context-menu-button']")
            threedot.click()
            time.sleep(2)
            self.SS("Three dot dropdown")
            threedot.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Three dots error %s", error)
            return self.threedots(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Three dots Menu",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function which opens advanced search drop down
    def advsearch(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            advasearch = self.driver.find_element_by_xpath("//i[@class = 'i-advanced-search']")
            advasearch.click()
            time.sleep(2)
            self.SS("Advanced Search")
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Advanced search error %s", error)
            return self.advsearch(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Advanced search",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function which opens data streaming bus tab
    def datastreamingbus(self,count,error,Pass,celladded):
        self.menuOpen(count,error,Pass,False)
        self.SS("Menu Open")
        try:
            datastreaminbus = self.driver.find_elements_by_xpath("//div[@class = 'siem-snap-menu-panel compressed']")
            datastreaminbus[11].click()
        except:
            time.sleep(5)
            datastreaminbus = self.driver.find_elements_by_xpath("//div[@class = 'siem-snap-menu-panel compressed']")
            datastreaminbus[11].click()
        time.sleep(20)
        frame = self.driver.find_element_by_xpath("//iframe[@class = 'mainframe']")
        self.driver.switch_to.frame(frame)
        time.sleep(2)
        try:
            add = self.driver.find_element_by_xpath("//i[@class = 'icon-plus']")
            add.click()
        except:
            time.sleep(5)
            add = self.driver.find_element_by_xpath("//i[@class = 'icon-plus']")
            time.sleep(10)
            add.click()
        time.sleep(2)
        self.SS("Data Streaming Slider")
        self.driver.switch_to.default_content()

    #function which opens first look feature tab
    def FLFeatures(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(3)
            self.menuOpen(count,error,Pass,False)
            time.sleep(3)
            flfeatures = self.driver.find_elements_by_xpath("//div[@class = 'siem-snap-menu-panel compressed']")
            flfeatures[12].click()
            time.sleep(3)
            return self.setup(count,error,Pass,False)
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("First Look Features error %s",error)
            time.sleep(3)
        if celladded == False:
            self.pdf.cell(40,20,"First Look Features",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function which opens setup button on the first look features page
    def setup(self,count,error,Pass,celladded):
        try:
            time.sleep(10)
            frame = self.driver.find_element_by_xpath("//iframe[@class ='mainframe']")
            self.driver.switch_to.frame(frame)
            time.sleep(2)
            setup = self.driver.find_element_by_xpath("//button[@class = 'landing-table__action lsg-btn-text btn-click']")
            setup.click()
            time.sleep(3)
            self.SS("Setup")
            self.enablers(count,error,Pass,False)
            print('123')
        except Exception as err:
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Setup error %s", error)
            time.sleep(3)
        if celladded == False:
            self.pdf.cell(40,20,"Setup",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded

    #function which clicks the different buttons in the setup page in first look features page
    def enablers(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            buttons = self.driver.find_elements_by_xpath("//div[@class ='mat-slide-toggle-thumb']")
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Enable button error %s", error)
            time.sleep(3)
        for i in buttons[:2]:
            time.sleep(2)
            i.click()
        time.sleep(3)
        self.SS("Buttons toggled")
        self.save(count,error,Pass,False)

    #test function for creating new pdfcell
    def addpdfcell(self,name,count,error,Pass,):
        self.pdf.cell(40,20,name,1,0,"C")
        if error != "None":
            self.pdf.set_font('Arial','B',4)
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.set_font('Arial','B',8)
        else:
            self.pdf.cell(40,20,error,1,0,"C")
        self.pdf.cell(40,20,str(count),1,0,"C")
        self.pdf.cell(40,20,Pass,1,1,"C")
    #function for clicking save button in the setup page
    def save(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            savebutton = self.driver.find_element_by_xpath("//button[@id = 'uc-slide-out-primary']")
            savebutton.click()
            time.sleep(3)
            self.SS("Save Button")
            confirm = self.driver.find_element_by_xpath("//div[@class = 'layout-main-body']")
            self.actions = ActionChains(self.driver)
            if self.flflag == False:
                self.actions.move_to_element_with_offset(confirm,400,400)
            else:
                time.sleep(2)
                print(True)
                self.actions.move_to_element_with_offset(confirm,330,400)
            self.actions.click()
            self.flflag = True
            self.actions.perform()
            self.driver.switch_to.default_content()
            self.actions.reset_actions()
            time.sleep(5)
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Save button error %s", error)
            time.sleep(3)
            return self.save(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell("Save Button",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function which loops through all tabs and opens them
    def addTab(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(2)
            self.openTab(count,error,Pass,False)
            time.sleep(2)
            self.SS("Open Tab Menu")
            self.openView(count,error,Pass,False)
            time.sleep(2)
            self.SS("Open View Menu")
            self.openDefault(count,error,Pass,False)
            time.sleep(2)
            self.SS("Open Default View Menu")
            views = self.driver.find_elements_by_xpath("//button[@class = 'uc-btn-clear uc-dropdown-group']")
            views[0].click()
            time.sleep(2)
            self.SS("Default View 1")
            for i in range(1,len(views)):
                iterateview = self.getTabs()
                time.sleep(4)
                iterateview[i].click()
                time.sleep(4)
                self.SS("Default View %i" %(i))
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("add Tab Error %s", error)
            return self.addTab(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"All Tabs Open",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded
    #function for changing the language
    def langchange(self,language,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            #sleeps the program, needed throughout program for letting things load
            time.sleep(10)
            #finding login username area
            usrname = self.driver.find_element_by_id("siemLoginUsername")
            usrname.click()
            usrname.send_keys(self.username)
            #finding password login area
            passwrd = self.driver.find_element_by_name("password")
            passwrd.click()
            passwrd.send_keys(self.password)
            #finding language change dropdown and changing language
            dropdown = self.driver.find_element_by_class_name("button-text")
            dropdown.click()
            lang = self.driver.find_element_by_xpath("//a[text()='%s']"%(language))
            lang.click()
            time.sleep(3)
            #screenshot function
            self.SS("Login Screen")
            #find logon button
            time.sleep(3)
            logon =  self.driver.find_element_by_class_name("siem-login-btn-wrapper")
            logon.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Login Error %s", error)
        time.sleep(10)
        self.SS("Landing Page")
        self.pdf.cell(40,20,"Language Change",1,0,"C")
        self.pdf.cell(40,20,error,1,0,"C")
        self.pdf.cell(40,20,str(count),1,0,"C")
        self.pdf.cell(40,20,Pass,1,1,"C")
        #function which calls all other functions in the program
        self.logoff(language)




    #function for opening the menu and opening each menu section
    def menuClicks(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        time.sleep(4)
        menuitems = self.driver.find_elements_by_xpath("//div[@class = 'siem-snap-menu-panel compressed']")
        openablemenuitems = [0,2,4,5,7,13,15,16,18]
        counter = 1
        for i in openablemenuitems:
            count = 0
            error = "None"
            Pass = "Pass"
            try:
                self.menuOpen(count,error,Pass,False)
                time.sleep(2)
                menuitems[i].click()
                time.sleep(5)
                self.SS("Menu Item %i" %(counter))
                counter +=1
            except Exception as err:
                self.timeoutcount +=1
                error = str(err)
                Pass = "Fail"
                count +=1
                print("Menu Item Open Error %s", error)
                pass
        if celladded == False:
            self.pdf.cell(40,20,"Menu Items Opened",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded


    #function for screenshotting
    def SS(self,name):
        self.driver.save_screenshot("Screenshots//%s//%s.png" % (self.currlang,name))
        self.counter1 += 1

    #function for clicking logoff button
    def LogOut(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            signout = self.driver.find_element_by_xpath("//span[@class = 'uc-icon i-sign-out']")
            signout.click()
            time.sleep(5)
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("logouterror", error)
            return self.LogOut(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Logout",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded


    #function for opening url to the login page
    def Logon(self):
        self.driver.get(self.urls)
        self.driver.maximize_window()


    #function for opening view tab
    def openView(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(10)
            X = self.driver.find_elements_by_xpath("//button[@class = 'uc-btn-clear uc-dropdown-group']")
            X[0].click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("openview error ", error)
            return self.openTab(count,error,Pass,celladded)
        if celladded == False and self.openviewrecorded == False:
            self.pdf.cell(40,20,"Open View",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            self.openviewrecorded = True
            celladded = True
            return celladded

    #function for opening default view tab
    def openDefault(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(3)
            defView = self.driver.find_elements_by_xpath("//span[@class = 'uc-sliding-menu-text']")
            defView[1].click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("open default view error ", error)
            return self.openTab(count,error,Pass,celladded)
        if celladded == False and self.opendefaultrecorded == False:
            self.pdf.cell(40,20,"Open Default Views",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            self.opendefaultrecorded = True
            celladded = True
            return celladded

    #function for opening menu
    def menuOpen(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(5)
            menu = self.driver.find_element_by_xpath("//span[@class = 'siem-menu-toggle i-menu']")
            menu.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            time.sleep(3)
            print("menuOpenerror ", error)
            test = self.driver.find_elements_by_xpath("//div[@class = 'siem-snap-menu-panel compressed']")
            if len(test)> 0:
                pass
            else:
                return self.menuOpen(count,error,Pass,celladded)
        if celladded == False and self.openmenurecorded == False:
            self.pdf.cell(40,20,"Open Menu ",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            self.openmenurecorded = True
            celladded = True
            return celladded


    #function for clicking the notification button
    def notificationOpen(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(3)
            noti = self.driver.find_element_by_xpath("//div[@class = 'i-notification-solid']")
            noti.click()
            time.sleep(3)
            self.SS("Notification Open")
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("notification open error ", error)
            return self.notificationOpen(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Notification Open",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded

    #function for opening dropdown containing logout button
    def ddownOpen(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            self.driver.switch_to.default_content()
            time.sleep(3)
            ddown = self.driver.find_element_by_xpath("//span[@class = 'i-user-person-solid']")
            ddown.click()
            time.sleep(2)
            self.SS("Logout Dropdown")
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("drop down Error ", error)
            return self.ddownOpen(count,error,Pass,celladded)
        if celladded == False:
            self.pdf.cell(40,20,"Logout Dropdown",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            celladded = True
            return celladded

    #function for opening add tab drop down menu
    def openTab(self,count,error,Pass,celladded):
        if self.timeoutcount >5:
            return
        try:
            time.sleep(2)
            tab = self.driver.find_element_by_xpath("//span[@translate = 'db.addTab']")
            tab.click()
        except Exception as err:
            self.timeoutcount +=1
            error = str(err)
            Pass = "Fail"
            count +=1
            print("Open tab error ", error)
            return self.openTab(count,error,Pass,celladded)
        if celladded == False and self.opentabrecorded == False:
            self.pdf.cell(40,20,"Open Tab",1,0,"C")
            self.pdf.cell(40,20,error,1,0,"C")
            self.pdf.cell(40,20,str(count),1,0,"C")
            self.pdf.cell(40,20,Pass,1,1,"C")
            self.opentabrecorded = True
            celladded = True
            return celladded
    #function which navigates to all available tabs and returns a list of the element references
    def getTabs(self):
        time.sleep(2)
        self.openTab(0,"None","Pass",False)
        time.sleep(2)
        self.openView(0,"None","Pass",False)
        time.sleep(2)
        self.openDefault(0,"None","Pass",False)
        time.sleep(2)
        defviews = self.driver.find_elements_by_xpath("//button[@class = 'uc-btn-clear uc-dropdown-group']")
        return defviews



#calls class/ initiates automation
#contains username password and ip address.
E = ESMCrawl("NGCP","Mcafee123$","https://10.25.118.72  ")
