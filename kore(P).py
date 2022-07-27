# 월요일
# 설악 2주전 월요일 9:00시 오픈
# 동원 주중 : 2주전 월요일 10:00분 오픈, 주말 : 2주전 금요일 10시:00분 오픈
# 여주 2주전 월요일 10시 30분 오픈
from cmath import log
from http.client import PAYMENT_REQUIRED
import time
from datetime import datetime
from turtle import ht
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pause
import pyperclip
import json
from bs4 import BeautifulSoup
import random
from tkinter import *

ID = "plzallyme"
PW = "alslvls82"
URL = ("https://www.koreapublic.co.kr/member/member_d.asp")




options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path='/Users/apple/chromedriver', options=options)
# driver.maximize_window()
wait = WebDriverWait(driver, 10)
# driver.get(URL)
# action = ActionChains(driver)




def getTime(timeString):
    textSplit = timeString.text.split(' ')
    if len(textSplit) > 2:
        try:
            timeInt = int(textSplit[1].replace(":", ""))
            return timeInt
        except ValueError:
            print(ValueError)
            return None

def login():    
    # driver.maximize_window()
    driver.get(URL)
    
    
    id_box = wait.until(EC.element_to_be_clickable((By.ID, "user_id")))
    pw_box = driver.find_element_by_id("user_pwd1")

    id_box.click()
    pyperclip.copy(ID)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    ActionChains(driver).reset_actions() #꼬일수도 있어서 action을 사용 후 리셋 해주기
    
    pw_box.click()
    pyperclip.copy(PW)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    ActionChains(driver).reset_actions()
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[3]/input'))).click()
    pyperclip.copy('')
    
    time.sleep(0.5)
    
    #접속 후 최초 나오는 팝업 닫기
    parent = driver.current_window_handle
    uselessWindows = driver.window_handles
    for winId in uselessWindows:
        if winId != parent: 
            driver.switch_to.window(winId)
            driver.close()
    driver.switch_to.window(parent)
    
    time.sleep(0.5)

def reserve():
    driver.get("https://www.koreapublic.co.kr/booking/booking01.asp")
    time.sleep(0.5)
    
    isFind = False
    
    canReserveDayList = []
    
    for i in range(1, 6):
        for j in range(1, 8):
            xPath = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td/table/tbody/tr[4]/td[1]/table/tbody/tr[' + str(i) + ']/td[' + str(j) + ']'
            dateBox = driver.find_element_by_xpath(xPath)
            imgs = dateBox.find_elements_by_tag_name('img')
            imgList = [img.get_attribute('src') for img in imgs]
            for img in imgList:
                if 're_yes.jpg' in img:
                    dateXPath = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td/table/tbody/tr[4]/td[1]/table/tbody/tr[' + str(i) + ']/td[' + str(j) + ']/table/tbody/tr[1]/td'
                    date = driver.find_element_by_xpath(dateXPath)
                    canReserveDayList.append({'xpath':xPath, 'day':date.text})
                    print('예약가능날짜 : ', date.text)
                    break
    
    canReserveList = []
    if len(canReserveDayList) > 0:
        for item in canReserveDayList:
            wait.until(EC.element_to_be_clickable((By.XPATH, item['xpath']))).click()
            table = driver.find_element_by_xpath('//*[@id="vovo1"]/tbody')
            list = table.find_elements_by_tag_name('tr')

            if len(list) > 0:
                for i in range(0, len(list)):
                    timeItem = list[i]
                    timeInt = getTime(timeItem)
                    if timeInt == None:
                        continue

                    if int(timeInt) >= 1200:
                        canReserveList.append(item)
                        table = driver.find_element_by_xpath('//*[@id="vovo1"]')
                        trs = table.find_elements_by_tag_name('tr') #예약 가능 티타임 수
                        rXPath = ''
                        
                        isWarning = False #3일전 예약인지 확인하기
                        textSplit = timeItem.text.split('(')
                        if len(textSplit) > 0:
                            timeSplit = textSplit[0].split('.')
                            if len(timeSplit) == 3:                                
                                today = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
                                target_date = datetime(int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))
                                d_day = target_date - today
                                if d_day.days < 3:
                                    isWarning = True
                                    continue #3일전 예약은 우선 막아 둠

                        if len(trs) == 1:
                            if isWarning:
                                rXPath = '//*[@id="vovo1"]/tbody/tr/td[5]/img'
                            else:
                                rXPath = '//*[@id="vovo1"]/tbody/tr/td[5]/input'
                        elif len(trs) > 1:
                            if isWarning:
                                rXPath = '//*[@id="vovo1"]/tbody/tr[{}]/td[5]/img'.format(i+1)
                            else:
                                rXPath = '//*[@id="vovo1"]/tbody/tr[{}]/td[5]/input'.format(i+1)

                        if len(rXPath) > 0:
                            try:
                                wait.until(EC.element_to_be_clickable((By.XPATH, rXPath))).click()
                                if isWarning:
                                  driver.switch_to.alert.accept() 
                            except ValueError:
                                rXPath = rXPath.replace("input", "img")
                                try:
                                    wait.until(EC.element_to_be_clickable((By.XPATH, rXPath))).click()
                                except ValueError:
                                    continue
                            finally:
                                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[6]/td/table/tbody/tr/td[1]/a/img'))).click()
                                driver.switch_to.alert.accept()
                                time.sleep(1)
                                driver.switch_to.alert.accept()
                                return


                                

            driver.back()


def getTypeFromHtml(html):
    strs = html.split()
    for str in strs:
        if "onclick" in str:
            subStrs = str.split(',')
            if len(subStrs) == 4:
                return subStrs[1].replace("'", "")
    return ""

def getDateFromHtml(html):
    strs = html.split()
    for str in strs:
        if "onclick" in str:
            subStrs = str.split(',')
            if len(subStrs) == 4:
                return subStrs[2].replace("'", "")
    return ""

def getTimeFromHtml(html):
    # return ("09:23".replace("'", "")).replace(":", "")
    strs = html.split()
    for str in strs:
        if "onclick" in str:
            subStrs = str.split(',')
            if len(subStrs) == 4:
                return (subStrs[3].replace("'", "")).replace(":", "")
    return ""

# def Ft2Cm():
#     driver.get(URL)
#     login()
#     # ft2cm = entry1.get()
#     # entry2.delete(0,"end")
#     # entry2.insert(0,round(float(ft2cm)*30.48,4))
# def Cm2Ft():
#     reserve()
#     # cm2ft = entry2.get()
#     # entry1.delete(0,"end")
#     # entry1.insert(0,round(float(cm2ft)/30.48,4))



def check():
    print('check')
    
def start():
    print(startEntry.get())
    print(endEntry.get())
    print(timeEntry.get())
    
    login()
    reserve()

def toggle():
    if toggleLb['text'] == "  OFF  ":
        # toggleBtn.configure(text="Stop")
        toggleLb.configure(text="  ON  ", bg="green")
    else:
        # toggleBtn.configure(text="Start")
        toggleLb.configure(text="  OFF  ", bg="red")






tk = Tk()

tk.title('코리아 퍼블릭 자동 예약 프로그램')
# tk.geometry('200x100')

Label(tk,text='시작일:ex)20220607 ').grid(row=0,column=0,padx=5)
Label(tk,text='종료일:ex)20220607 ').grid(row=1,column=0,padx=5)
startEntry = Entry(tk)
endEntry = Entry(tk)
startEntry.grid(row=0,column=1)
endEntry.grid(row=1,column=1)

Label(tk,text='예약시간: ').grid(row=2, column=0,padx=5)
timeEntry = Entry(tk)
timeEntry.grid(row=2,column=1)

# Label(tk,text='마감임박 예약 여부: ').grid(row=3, column=0,padx=5)

toggleBtn = Button(tk, text="마감임박 예약", command=toggle)
toggleBtn.grid(row=3,column=0)

toggleLb = Label(tk, text="  OFF  ", bg="red")
toggleLb.grid(row=3,column=1)


button = Button(tk,text='    자동 예약 시작    ', bg='red', fg='green', command=start).grid(row=4,column=0, columnspan=4, padx=20, pady=20)

tk.mainloop()

  
# def main():
#     print()
    

#     login()




# if __name__ == "__main__":
#     main()
