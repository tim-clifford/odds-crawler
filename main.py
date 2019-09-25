import time
import pickle
import threading
from collections import OrderedDict
from queue import Queue
from selenium import webdriver
from bs4 import BeautifulSoup
import calc
from bookies import *
from Matcher import matched_options

backs = [Ladbrokes(),Eight(),Virgin()]
lays = [Smarkets()]
back_queue = Queue()
lay_queue = Queue()
threads = [
    threading.Thread(
            target=x.get_events,
            name="Thread_{}".format(x.name),
            args=[back_queue],
        ) for x in backs
] + [
    threading.Thread(
            target=x.get_events,
            name="Thread_{}".format(x.name),
            args=[lay_queue],
        ) for x in lays
]
for t in threads: t.start()
for t in threads: t.join()

back_events = []
lay_events = []
while not back_queue.empty(): back_events.append(back_queue.get_nowait())
while not lay_queue.empty(): lay_events.append(lay_queue.get_nowait())

pickle.dump((back_events,lay_events),open("tests.p","wb"))
'''
back_events,lay_events = pickle.load(open("tests.p","rb"))
'''
options = matched_options(back_events,lay_events)

options_str = [str(x) for x in sorted(options,key=lambda x: x.profit_ratio)]#,reverse=True)]
#open("results.md","w").write
print("\n".join(list(OrderedDict.fromkeys(options_str))))
