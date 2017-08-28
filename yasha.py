# coding: utf-8
import random
import sys
import time

from selenium import webdriver

search_text = 'купить модульную азс б/у'

driver = webdriver.Firefox()
driver.implicitly_wait(10)

driver.get('http://ya.ru')

all_suggestions = set()

inputElement = driver.find_element_by_id('text')
for char in search_text:
    inputElement.send_keys(char)
    time.sleep(random.random())

    try:
        all_suggestions.update({suggestion.text for suggestion in
                                driver.find_elements_by_css_selector('span.suggest2-item__text')})
    except Exception as e:
        print(e.args)
        pass

inputElement.submit()

print('all_suggestions', all_suggestions)
sys.exit(0)

time.sleep(10)

all_serp_items = driver.find_elements_by_class_name('serp-item')
organic_list = [li for li in all_serp_items if 't-construct-adapter__legacy' in li.get_attribute('class')]
print('links', len(organic_list))

related = driver.find_elements_by_css_selector('div.related > div > div.related__item')
related_text = [rel_text.text for rel_text in related]
print('related', related_text)

pagination = driver.find_elements_by_css_selector('div.pager > a')
print('pagination', [page.text for page in pagination])

for place, li in enumerate(organic_list):
    print('место', place + 1)
    title = li.find_element_by_css_selector('h2').text
    print(title)
    subtitle = li.find_element_by_css_selector('div.organic__path').text
    print(subtitle)
    snippet = li.find_element_by_css_selector('div.organic__content-wrapper').text
    print(snippet)

    link = li.find_element_by_css_selector('h2 > a')
    print(link)

    builder = ActionChains(driver)
    builder.move_to_element(li).click(link).perform()



    # driver.close()
