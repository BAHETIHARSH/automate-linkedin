import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver

import credentials

queued = []
login_id = credentials.loginid
password = credentials.password


def write_list(users):
    f = open("connections.txt", "a")
    for j in users:
        if 'contact' in j or 'detail' in j:
            continue
        f.write(j.split('"')[1][1:-1] + "\n")
        queued.append(j.split('"')[1][1:-1])


def links():
    driver.get("https://www.linkedin.com/mynetwork/")
    time.sleep(20)

    html = driver.page_source
    # driver.close()
    bst = BeautifulSoup(html, features="html.parser")
    user_links = re.findall('href="/in/.[^"]*"', str(bst))
    write_list(user_links)


def login():
    email = driver.find_element_by_xpath("//*[@id='session_key']")
    email.send_keys(login_id)

    email = driver.find_element_by_xpath("//*[@id='session_password']")
    email.send_keys(password)

    email = driver.find_element_by_xpath("//*[@id='main-content']/section[1]/div[2]/form/button")
    email.click()


def send_connection(user):
    try:
        driver.get(url + user)
        time.sleep(2)
        connect = driver.find_element_by_xpath(
            "/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[1]/div["
            "2]/div/div/div[1]/div/button/span")

        if connect.text == "Connect":
            connect.click()
            send = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
            send.click()
        print("send requested : ", user)
    except:
        print("Error :", user)
        send_connection(user)


url = "https://www.linkedin.com/"
driver = webdriver.Chrome(executable_path=".\\chromedriver.exe")
driver.get(url)
login()
print("login successfully")
for _ in range(1):
    links()
    print("links generated")
    for i in queued:
        print(i)
        send_connection(i)
        # send_connection(i)
        time.sleep(2)

driver.close()
