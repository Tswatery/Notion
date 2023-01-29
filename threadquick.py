import threading
import queue
import requests
from bs4 import BeautifulSoup

data_queue = queue.Queue()
data_lock = threading.Lock()
url_queue = queue.Queue()

def worker():
    while 1:
        url = url_queue.get()
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        with data_lock:
            data_queue.put((soup.find('title').text, url))
        url_queue.task_done()

def main(url_list):
    for _ in range(10):
        t = threading.Thread(target = worker)
        t.daemon = True
        t.start()

    for url in url_list:
        url_queue.put(url)

    url_queue.join()
    res = []

    while not data_queue.empty():
        data = data_queue.get()
        res.append(data)

    return res