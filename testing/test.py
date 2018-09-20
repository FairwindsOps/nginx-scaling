#!/usr/bin/env python2
#https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python

from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue
import time

concurrent = 500
start_time = time.time()
errors = {}
successes = {}

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    if not status is 200:
        errors[url] = status
    else:
        successes[url] = status

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('hosts.txt'):
        url = "http://{}".format(url)
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
end_time = time.time()
print("There were {} errors and {} successes.".format(len(errors), len(successes)))
print("This loop to {} seconds.".format(end_time - start_time))
