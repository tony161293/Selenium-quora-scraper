from selenium import webdriver
import os, time, csv
import psycopg2
from config import config

def write(sentance):
    time.sleep(5)
    browser.find_element_by_xpath("//textarea[@class='textarea']").clear()
    browser.find_element_by_xpath("//textarea[@class='textarea']").send_keys(sentance)
    time.sleep(10)

    cards_col = browser.find_element_by_xpath("//div[@class='_adbfa1e6-editor-page-cardsCol']") #cards col
    list_of_cards = cards_col.find_elements_by_xpath(".//div[@class='cardBaseClassName _72569e-card _72569e-cardCollapsed _72569e-animatePosition']")
    
    for x in list_of_cards:
        try:
            x.find_element_by_xpath(".//span[@class='_ed4374-buttonWrapper _ed4374-headerButton _ed4374-btnExpand']").click() #down arrow
            time.sleep(2)
            x.find_element_by_xpath(".//span[@class='_83a2be-footerButton _83a2be-btnMore']").click() #more button
            time.sleep(2)
            short_desc = x.find_element_by_xpath(".//p[@class='_bbb203ba-card-shortDesc']").get_attribute('innerHTML').decode('latin-1').encode('UTF8')
            long_description = x.find_element_by_xpath(".//div[@class='_a9e93e07-card-long']/div").get_attribute('innerHTML').decode('latin-1').encode('UTF8')
            description = short_desc + long_description
            sql = "INSERT INTO errors(description) VALUES(%s);"
            cur.execute(sql, (description,))
            x.find_element_by_xpath(".//span[@class='_929504-insertReplacement']").click() #replace button
        except:
            pass

    corrected = browser.find_element_by_xpath("//textarea[@class='textarea']").get_attribute('value').decode('latin-1').encode('UTF8')
    sql_output = "INSERT INTO corrections(wrongs, rights) VALUES (%s, %s);"
    cur.execute(sql_output, (sentance.decode('latin-1').encode('UTF8'), corrected,))
    conn.commit()

url = 'https://www.grammarly.com/signin'
chrome_driver = '/usr/local/bin/chromedriver'
os.environ["webdriver.chrome.driver"] = chrome_driver
browser = webdriver.Chrome(chrome_driver)
browser.get(url)
time.sleep(2)

username = 'mailmemaisie@gmail.com'
pasword = 'maisiegreen123'

browser.find_element_by_xpath("//input[@data-qa='txtEmail']").send_keys(username)
browser.find_element_by_xpath("//input[@data-qa='txtPassword']").send_keys(pasword)
time.sleep(4)
browser.find_element_by_xpath("//button[@class='_4c31bd-basicButton _4c31bd-schemeGreen _4c31bd-shapeRound _4c31bd-sizeLarge _2030ff-button']").click() #login button
time.sleep(10)
# ipdb.set_trace()
sentance_list = [x['input'] for x in csv.DictReader(open('input.csv'))]
output_list = []
description_list = []
browser.get('https://app.grammarly.com/docs/200375454')

conn = None
try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    [write(x) for x in sentance_list]

    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')
