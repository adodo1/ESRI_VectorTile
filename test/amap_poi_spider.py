#!/usr/bin/env python
# encoding: utf-8

import os, sys, json, requests
import threading, Queue
from threading import Thread


mutex = threading.Lock()        # thread lock !


##########################################################################
##########################################################################
##########################################################################
class Worker(Thread):
    # 线程池工作线程 只支持 python 2.7 或以上版本
    worker_count = 0
    def __init__(self, workQueue, resultQueue, timeout = 0, **kwds):
       Thread.__init__(self, **kwds)
       self.id = Worker.worker_count
       Worker.worker_count += 1
       self.setDaemon(True)
       self.workQueue = workQueue
       self.resultQueue = resultQueue
       self.timeout = timeout
       self.start()
     
    def run(self):
        ''' the get-some-work, do-some-work main loop of worker threads '''
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                #print "worker[%2d]: %s" % (self.id, str(res))
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except :
                print 'worker[%2d]' % self.id, sys.exc_info()[:2]

class WorkerPool:
    # 线程池
    def __init__(self, num_of_workers=10, timeout = 1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_of_workers)
    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers): 
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)
    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        #print "All jobs are are completed."
    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))
    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

##########################################################################
##########################################################################
##########################################################################
    

def test(num):
    url = 'http://lbs.amap.com/dev/api?keywords=银行&types=160000&city=柳州&children=1&offset=20&page={0}&extensions=all'.format(num)
    headers = {
        #'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Origin': 'http://lbs.amap.com',
        #'Referer': 'http://lbs.amap.com/api/webservice/guide/api/search/',
        'X-Requested-With': 'XMLHttpRequest',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        #'Accept-Encoding': 'gzip, deflate',
        #'Accept-Language': 'zh-CN,zh;q=0.8',
        #'Cookie': cookie
    }

    data = {
        'type': 'place/text',
        'version': 'v3'
    }


    r = requests.post(url, headers=headers, data=data)
    data = json.loads(r.content)
    mutex.acquire()
    print num, data['count'], data['info'], data['pois'][0]['name']
    mutex.release()

if __name__=='__main__':
    print '[==DoDo==]'
    print 'get amap pois.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    wp = WorkerPool(20)

    for n in range(0, 100):
        for i in range(1, 45):
            #test(i)
            wp.add_job(test, i)

    wp.wait_for_complete()

    '''
    cookie = open('./cookie.txt', 'r').read()
    
    url = 'http://lbs.amap.com/dev/api?keywords=银行&types=160000&city=柳州&children=1&offset=20&page=2&extensions=all'
    headers = {
        #'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Origin': 'http://lbs.amap.com',
        #'Referer': 'http://lbs.amap.com/api/webservice/guide/api/search/',
        'X-Requested-With': 'XMLHttpRequest',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        #'Accept-Encoding': 'gzip, deflate',
        #'Accept-Language': 'zh-CN,zh;q=0.8',
        #'Cookie': cookie
    }

    data = {
        'type': 'place/text',
        'version': 'v3'
    }

    
    print cookie
    r = requests.post(url, headers=headers, data=data)
    data = json.loads(r.content)
    print data['count'], data['info']
    '''









