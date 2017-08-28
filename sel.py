# coding: utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
import time
from cred import *
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('start')

fp = webdriver.FirefoxProfile()
fp.set_preference('browser.download.dir', '/home/sanya/Загрузки')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                  "application/octet-stream,text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel")
driver = webdriver.Firefox(firefox_profile=fp)

driver.get("http://{login}:{password}@{url}".format(login=login, password=password, url=url))

inputElement = driver.find_element_by_name("login")
inputElement.send_keys(second_login)

inputElement = driver.find_element_by_name("password")
inputElement.send_keys(second_login)

driver.find_element_by_name("ok").click()

print(driver.title)

driver.find_element_by_link_text('Заказы').click()

print(driver.title)

# установим select - статус заказа="не важно"
order_status = Select(driver.find_element_by_name('s_status_id'))
order_status.select_by_visible_text("не важно")

# нажмем на кнопку Найти
driver.find_elements_by_xpath('//input[@value="Найти"]')[0].click()

# выберем все заказы (без пагинации)
# driver.find_element_by_link_text('Все').click()

pages = driver.find_elements_by_css_selector('div#main > p:nth-child(5) > a.pages')
#main > p:nth-child(5)
# pages = set(pages)
print('pages len', len(pages))


for l in pages:
    print(l.text, l.get_attribute('href'))

# div#main > p > a.pages

logging.debug('sleep while page loading')
time.sleep(10)
logging.debug('wake and ready for parse')

main_window = driver.current_window_handle

logging.debug('start collecting links')
orders_list = driver.find_elements_by_css_selector('table#list > tbody > tr > td:nth-child(3) > a')
logging.debug('end of links collecting')

# WebDriverWait(driver, 100).until(
#     lambda driver: driver.find_element_by_name(self.locator))
# driver.find_element_by_name(self.locator).send_keys(value)

# print orders_list
for el in orders_list:
    # print el, el.get_attribute('href')
    logging.debug(el.text)
    # открываем новую вкладку
    el.click()
    time.sleep(2)

    # for w in driver.window_handles:
    #     print 'window:', w
    logging.debug('opened windows:', len(driver.window_handles))
    logging.debug('window title:', driver.title)

    # for win in driver.window_handles:
    #     print(win)

    # actions = ActionChains(driver)
    # actions.key_down(Keys.CONTROL).key_down('w').key_up('w').key_up(Keys.CONTROL).perform()

    # driver.switch_to.active_element()
    # ael = driver.switch_to.active_element
    # print ael
    # driver.switch_to.window('Содержимое заказа. Администрирование сайта admin.vidumshiki.ru')
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    logging.debug('switch to window', driver.title)
    driver.find_element_by_link_text('Скачать в Excel').click()
    time.sleep(1)
    # alert = driver.switch_to.alert()
    # print(alert)
    # alert.accept()

    driver.close()

    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    # el.send_keys(Keys.CONTROL + Keys.RETURN)
    # print 'new tab:', driver.current_window_handle
    # жмём скачать файл

    # print driver.find_elements_by_css_selector('#tabm > li > a')

    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

    # Put focus on current window which will, in fact, put focus on the current visible tab
    driver.switch_to.window(main_window)
    time.sleep(2)

    logging.debug('main window title:', driver.title)
    # driver.close()

    # Close current tab
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    # driver.switch_to_window(main_window)

    time.sleep(5)
