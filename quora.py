from selenium import webdriver
import os, time, csv, ipdb
import psycopg2
from config import config
from unidecode import unidecode


url = 'https://www.quora.com'
chrome_driver = '/home/paul/Downloads/chromedriver'
os.environ["webdriver.chrome.driver"] = chrome_driver
browser = webdriver.Chrome(chrome_driver)
browser.get(url)
time.sleep(2)


username = "mailmemaisie@gmail.com"
password = "maisiegreen123"
browser.find_elements_by_xpath("//input[@class='text header_login_text_box ignore_interaction']")[0].send_keys(username)
browser.find_elements_by_xpath("//input[@class='text header_login_text_box ignore_interaction']")[1].send_keys(password)
time.sleep(3)
browser.find_element_by_xpath("//input[@class='submit_button ignore_interaction']").click()
time.sleep(5)


# url = raw_input("Enter the topic url");
url = "https://www.quora.com/topic/Blog-Writing-1"
browser.get(url)
for i in range(0, 40):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

qns = browser.find_elements_by_xpath("//a[@class='question_link']")
urls = [a.get_attribute('href').encode('utf8') for a in qns]
def write(u):
    browser.get(u)
    time.sleep(2)
    for i in range(0, 10):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    text_list = browser.find_elements_by_xpath("//p[@class='qtext_para']")
    time.sleep(2)
    text = [unidecode(x.text) for x in text_list]
    for desc in text:
        sql = "INSERT INTO quora(description) VALUES(%s);"
        try:
            cur.execute(sql, (desc,))
            conn.commit()
        except:
            # print(ex)
            conn.rollback()
            # print "Execution error, rollback"

conn = None
try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    [write(x) for x in urls]

    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')
        browser.close()
