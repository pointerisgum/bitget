# 월요일
# 설악 2주전 월요일 9:00시 오픈
# 동원 주중 : 2주전 월요일 10:00분 오픈, 주말 : 2주전 금요일 10시:00분 오픈
# 여주 2주전 월요일 10시 30분 오픈
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
import telegram

teleToken = "5576180085:AAG3ScxRpEqjBdcbAW9hfQm3NRsafKqePhI"
chatId = "-752551139"
bot = telegram.Bot(token=teleToken)

# updates = bot.getUpdates()
# for u in updates:
#     if u is None:
#         continue
#     if u.message is None:
#         continue
#     if u.message['chat'] is None:
#         continue
#     print(u.message['chat']['id'])

# bot = telegram.Bot(token = teleToken)
# text = 'asdasdsd'
# bot.sendMessage(chat_id = chatId, text=text)

ID = "38003700"
PW = "3585sky12*"
URL = ("https://www.sunvalley.co.kr/member/login?returnURL=/reservation/golf")

now = datetime.now()
options = Options()
options.headless = False

driver = webdriver.Chrome(
    executable_path='/Users/apple/chromedriver',
    options=options)
# driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get(URL)
action = ActionChains(driver)
# time.sleep(5)

def login():
    id_box = wait.until(EC.element_to_be_clickable((By.ID, "usrId")))
    pw_box = driver.find_element_by_id("usrPwd")

    id_box.click()
    pyperclip.copy(ID)
    action.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    action.reset_actions() #꼬일수도 있어서 action을 사용 후 리셋 해주기
    
    pw_box.click()
    pyperclip.copy(PW)
    action.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    action.reset_actions()
    login = wait.until(EC.element_to_be_clickable((By.ID, "fnLogin"))).click()

    # action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
    # action.reset_actions()
    # time.sleep(1.5)
    # action.send_keys(Keys.SPACE)
    # action.reset_actions()

    pyperclip.copy('')
    
    time.sleep(0.5)
    
    driver.switch_to.alert.accept()
    
def reserve(clubId):
    print('검색 시작')
    # loginBtn = wait.until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "gnb_btn_login"))).click()

    # id_box = wait.until(EC.element_to_be_clickable((By.ID, "usrId")))
    # pw_box = driver.find_element_by_id("usrPwd")

    # id_box.click()
    # pyperclip.copy(ID)
    # action.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    # action.reset_actions() #꼬일수도 있어서 action을 사용 후 리셋 해주기
    
    # pw_box.click()
    # pyperclip.copy(PW)
    # action.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()
    # action.reset_actions()
    # login = wait.until(EC.element_to_be_clickable((By.ID, "fnLogin"))).click()

    # # action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
    # # action.reset_actions()
    # # time.sleep(1.5)
    # # action.send_keys(Keys.SPACE)
    # # action.reset_actions()


    # pyperclip.copy('')
    
    # time.sleep(0.5)
    
    # driver.switch_to.alert.accept()
    

    # time.sleep(1.5)
    
    #설악:21
    #썬밸리:23
    #동원:24
    #여주:25
    # driver.get("https://www.sunvalley.co.kr/reservation/golf?sel=J24")
    
    #아이디는 #으로
    #class는 .으로
    

    wait.until(EC.element_to_be_clickable((By.ID, clubId))).click()
    time.sleep(0.5)
    
    # clubIds = ["selectCoIdJ21", "selectCoIdJ24", "selectCoIdJ25"]
    # while True:
    #     for clubId in clubIds:
    #         try:
    #             wait.until(EC.element_to_be_clickable((By.ID, clubId))).click()
    #             time.sleep(1)
    #         except ValueError:
    #             continue
            
    #         try:
    #             lives = driver.find_elements_by_css_selector(".cal_live")
    #             print(lives)
    #             if len(lives) > 0:
    #                 print("예약 가능한게 있음")
    #             else:
    #                 print(clubId, "풀 예약")
                    
    #             time.sleep(1)
    #         except ValueError:
    #             continue





    # driver.find_element_by_css_selector("#selectCoIdJ24").click()
        
    # print(ends)
    
    # wait.until(EC.element_to_be_clickable((By.ID, "B20220713"))).click()

    # # driver.find_element_by_css_selector("#B20220713").click()
    # time.sleep(10)
    
    # testcnt = 1
    
    #날짜선택 (입력받을 값)
    startDate = "20220629"
    endDate = "20220629"
    
    startTime = "0600"  #보다 같거나 크고
    endTime = "0900"    #보다 같거나 작을때
    
    # table1 = driver.find_elements_by_css_selector(".cm_calender_tbl")
    calTables = driver.find_elements(By.CLASS_NAME, 'cm_calender_tbl')
    for calTable in calTables:
        trs = calTable.find_elements(By.TAG_NAME, "tr")
    # row = rows[1]
    # col = row.find_elements(By.TAG_NAME, "td")[1]
        for tr in trs:
            try:  
                tds = tr.find_elements(By.TAG_NAME, "td")
                for td in tds:
                    html = td.get_attribute("innerHTML")
                    if len(html) > 0:
                        date = getDateFromHtml(html)
                        if int(startDate) <= int(date) and int(endDate) >= int(date):
                            #선택 된 기간만 검색
                            
                            rTime = getTimeFromHtml(html)
                            if "CLOSE" in rTime or "NOOPEN" in rTime :
                                print('잔여티 없음')
                                continue
                            
                            # try:
                            #     timeInt = int(rTime)
                            #     print(timeInt)
                            # except ValueError:
                            #     print(ValueError)
                            #     continue

                            
                            if "cal_live" in html:
                                #시간 조건 검색
                                # if int(timeInt) >= int(startTime) and int(timeInt) <= int(endTime):
                                #     print("!!find!!", date, getTimeFromHtml(html))

                                #예약가능한 날짜의 아이디 구하기 ex)A20220607 (A는 현재 선택된달, B는 다음달)
                                calDateId = getTypeFromHtml(html) + getDateFromHtml(html)
                                
                                if len(calDateId) > 0 :
                                    wait.until(EC.element_to_be_clickable((By.ID, calDateId))).click()
                                    
                                    reserveTables = driver.find_elements(By.CLASS_NAME, 'tbl-group')
                                    for reserveTable in reserveTables:
                                        trList = reserveTable.find_elements(By.TAG_NAME, "tr")
                                        for trDetail in trList:
                                            reserveTds = trDetail.find_elements(By.TAG_NAME, "td")
                                            if len(reserveTds) > 1:
                                                if reserveTds[-1].text == "신청" and len(reserveTds[3].text) > 0:
                                                    rTime = (reserveTds[3].text).replace(":", "")
                                                    try:
                                                        timeInt = int(rTime)
                                                        print(timeInt)
                                                    except ValueError:
                                                        print(ValueError)
                                                        continue
                                                    
                                                    if int(timeInt) >= int(startTime) and int(timeInt) <= int(endTime):
                                                        #시간 조건이 충족 할 경우 예약
                                                        msg = reserveTds[0].text + " " + reserveTds[3].text
                                                        # print(msg)
                                                        
                                                        clubName = ''
                                                        if '21' in clubId:
                                                            clubName = '설악'
                                                        elif '24' in clubId:
                                                            clubName = '동원'
                                                        elif '25' in clubId:
                                                            clubName = '여주'

                                                        xPath = '//*[@id="tabCourseALL"]/div/div/table/tbody/tr[" + reserveTds[0].text + "]/td[" + str(int(calDateId[5] + calDateId[6])) + "]/button'
                                                        print("xPath : ", xPath)
                                                        driver.find_element_by_xpath(xPath).click()
                                                        time.sleep(0.5)
                                                        driver.find_element_by_xpath('//*[@id="golfTimeDiv2"]/div[3]/div/div[1]/button').click()
                                                        time.sleep(0.5)

                                                        totalMsg = msg + " " + clubName + ' 예약완료'
                                                        print(totalMsg)
                                                        bot.sendMessage(chat_id = chatId, text=totalMsg)
                                                        
                                                        driver.switch_to.alert.accept()
                                                        time.sleep(0.5)
                                                        driver.get("https://www.sunvalley.co.kr/reservation/golf")
                                                        
                                                        
                                                        return True

                                                    # if testcnt == 3:
                                                    #     driver.find_element_by_css_selector(".btn.btn-res").click()
                                                    # testcnt+=1
                                                    # driver.find_element_by_xpath("//*[@id='tabCourseALL']/div/div/table/tbody/tr[8]/td[6]/button").click()

                                        #     for reserveTd in reserveTds:
                                        #         print(reserveTd.text)
                                        # else:
                                        #     print("예약 가능한 날이 없음")
                                
                                
                                
                                
                                
                                
                                
                                
                    # if len(html) > 0:
                    #     soup = BeautifulSoup(html, 'html.parser')
                    #     soup.body.a.text
                    #     val = soup.input['onclick']
                    #     print(val)

            except ValueError:
                print(ValueError)
                continue
            # print(col.text) #prints text from the element

    # //*[@id="tabCourseALL"]/div/div/table/tbody/tr[9]/td[6]/button
    # //*[@id="tabCourseALL"]/div/div/table/tbody/tr[10]/td[6]/button
    # //*[@id="tabCourseALL"]/div/div/table/tbody/tr[19]/td[6]/button
    # //*[@id="tabCourseALL"]/div/div/table/tbody/tr[30]/td[6]/button
    # a = driver.find_element_by_css_selector("#calendar_view_ajax_1")
    # cal = driver.find_elements_by_css_selector(".cm_calender_tbl")
    # list1 = cal[0].find_elements_by_tag_name("td")
    # aa = driver.find_elements_by_css_selector("#d5b6a011-90ea-4b0a-ab17-566ce032a18a")
    # print(aa)
    # # list1 = cal[0].find_element_by_tag_name("tbody")
    # # list1.find_element_by_tag_name("tr")
    
    # print(list1)
    # print(cal[0])
    # print(cal[1])
    
    # t = driver.find_elements_by_css_selector(".drop-item")
    # print(t[2].text)
    # t2 = driver.find_element_by_css_selector("#selectCoIdJ24").click()
    # print(t2.text)
    
    # wait.until(EC.element_to_be_clickable((By.ID, "selectCoIdJ24"))).click()
    
    # # calender1 = driver.find_element_by_css_selector('div[class="calendar_view_ajax_1"]')
    # list1 = driver.find_element_by_xpath("//*[@id='calendar_view_ajax_1']")
    # list2 = driver.find_element_by_xpath("//*[@id='calendar_view_ajax_2']")

    # list = driver.find_element_by_class_name('cm_calender_tbl')

    # val = list.find_elements_by_tag_name("tbody")    
    # val2 = val.find_elements_by_tag_name("tr")
    # val3 = val2.find_element_by_id("A20220601")
    # # val1 = list.find_element_by_class_name("tbody")

    # area1 = calender1.find_element_by_id('cm_calender_tbl')
    # area = area1.find_elements_by_tag_name('tbody')


    # wait.until(EC.element_to_be_clickable((By.ID, "A20220615"))).click()
    # wait.until(EC.element_to_be_clickable((By.ID, "A20220615"))).click()

    
    # agree_btn = driver.find_element_by_xpath(
    # "//div[@class='section_booking_agreement']/div[@class='agreement all']/label"
    # ).click()
#content > div.content-body > div.tap_inner > ul > li:nth-child(2) > a > span > em


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


# def wait_booking():
#     booking_btn = 0

#     while True:

#         try:
#             print("try")
#             more_info = wait.until(
#                 EC.element_to_be_clickable(
#                     (By.CSS_SELECTOR, 'span[ng-bind-html="bizItemInfo.name | newlines"]')))
#             booking_btn = driver.find_element_by_css_selector(
#                 'span[ng-bind-html="bizItemInfo.name | newlines"]')
#         except:
#             driver.refresh()
#             print("refresh")
#             time.sleep(0.5)
#         if booking_btn != 0:
#             break

#     booking_btn.click()

# def get_calender():

#     calendar = wait.until(EC.element_to_be_clickable((By.ID, "calendar")))

#     month = calendar.find_element_by_css_selector(
#         'span[ng-bind="$ctrl.baseDate.get(\'month\') + 1"]')

#     print(month.text)

#     nobth_sel_btn_R = calendar.find_element_by_css_selector(
#         'a[ng-click="$ctrl.nextMonth()"]')
#     nobth_sel_btn_L = calendar.find_element_by_css_selector(
#         'a[ng-click="$ctrl.prevMonth()"]')

#     if month.text == str(now.month):
#         nobth_sel_btn_R.click()

#     return calendar


# def make_booking(calendar):

#     # wait.until(
#     #     EC.text_to_be_present_in_element(
#     #         (By.CSS_SELECTOR, 'span[ng-bind="$ctrl.getDay(key)"]'), "12"))

#     time.sleep(0.5)

#     calendar_table = calendar.find_element_by_class_name("tb_body")
#     weeks = calendar_table.find_elements_by_tag_name("tr")

#     sat_date = []
#     sun_date = []
#     etc_date = []

#     for item in weeks:
#         days = item.find_elements_by_tag_name("td")
#         for item2 in days:
#             class_attribute = item2.get_attribute("class")
#             if class_attribute == "calendar-sat":
#                 sat_date.append(item2)
#             elif class_attribute == "calendar-sun":
#                 sun_date.append(item2)
#             else:
#                 etc_date.append(item2)

#     sat_date[1].click()

#     ###
#     time.sleep(0.1)
#     customer_selector = wait.until(
#         EC.element_to_be_clickable((By.CLASS_NAME, "customer_selector")))
#     time_select_am = customer_selector.find_element_by_css_selector(
#         'div[class="am"]'
#     ).find_elements_by_css_selector('span[ng-bind="$ctrl.getStartTime(timeSchedule)"]')
#     time_select_pm = customer_selector.find_element_by_css_selector(
#         'div[class="pm"]'
#     ).find_elements_by_css_selector('span[ng-bind="$ctrl.getStartTime(timeSchedule)"]')

#     time_select = [time_select_am, time_select_pm]

#     time_select[1][0].click()

#     agree_btn = driver.find_element_by_xpath(
#         "//div[@class='section_booking_agreement']/div[@class='agreement all']/label"
#     ).click()
#     gogo_btn = driver.find_element_by_css_selector(
#         "button[ng-click='$ctrl.clickSubmit($event)']").click()

#     pop_up = wait.until(
#         EC.element_to_be_clickable((
#             By.CSS_SELECTOR,
#             'div[class="popup_booking application notify app_notice confirm_type"]'
#         )))

#     if pop_up.text.split('\n')[0] == "예약이 확정되었습니다.":
#         print("success!!\n")
#         return 1
#     else:
#         print("fail..\n")
#         return 0


def main():

    result = 0

    login()
    # reserve("selectCoIdJ21")

    # clubIds = ["selectCoIdJ21", "selectCoIdJ24", "selectCoIdJ25"]
    clubIds = ["selectCoIdJ24", "selectCoIdJ25"]
    while True:
        for clubId in clubIds:
            success = reserve(clubId)
            if success is not None and success == True:
                print('예약 성공 프로그램 종료')
                return
            
            sleepTime = random.randrange(1,10)
            # print('refresh time : ', sleepTime)
            time.sleep(sleepTime)
            
    time.sleep(9999999)
    # wait_booking()
    # calendar = get_calender()

    # while result != 1:
    #     result = make_booking(calendar)


if __name__ == "__main__":
    main()
