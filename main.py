import time
import random
import logging
import threading
import webbrowser
from selenium import webdriver


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s')

time_break = 30.0

urls = [
    'https://datohost.com/vi?banner_title=Smart%20URL:%20t%E1%BB%B1%20%C4%91%E1%BB%93ng%20thay%20%C4%91%E1%BB%95i%20n%E1%BB%99i%20dung%20theo%20tham%20s%E1%BB%91%20%C4%91%C6%B0%E1%BB%9Dng%20d%E1%BA%ABn',
    'https://datohost.com/vi?banner_title=Kh%C3%B4ng%20gi%E1%BB%9Bi%20h%E1%BA%A1n%20s%E1%BB%91%20l%C6%B0%E1%BB%A3ng%20Landing%20Page',
    'https://datohost.com/vi?banner_title=Qu%E1%BA%A3ng%20c%C3%A1o%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20tr%C3%AAn%20Google%20v%C3%A0%20Facebook'
]
# urls = [
#     'http://localhost:8096/',
#     'http://localhost:8096/create_user'
# ]


def send_request():
    threading.Timer(time_break, send_request).start()
    i = random.randrange(len(urls))
    logging.info('url {no}: {url}'.format(no=i, url=urls[i]))
    # response = requests.get(urls[i])
    # if response.status_code != 200:
    #     logging.info(response.content.decode())
    # webbrowser.open(urls[i])
    driver = webdriver.Chrome()
    j = random.randrange(3)
    for k in range(j):
        time.sleep(1)
        driver.get(urls[i])
    time.sleep(5)
    driver.close()


send_request()
