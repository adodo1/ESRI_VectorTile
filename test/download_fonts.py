#!/usr/bin/env python
# encoding: utf-8

import os, sys, math, requests, time
import socket, threading, json, Queue
from threading import Thread

# 1. input a extent like: tid, minX maxX, minY, maxY, zoom
# 2. cal total of mission, add thread to work list, and show proess
# 3. the sp use web mercator x: [ -20037508.3427892, 20037508.3427892 ]

# globel vars
mutex = threading.Lock()        # thread lock !
socket.setdefaulttimeout(20)    # outtime set 20s
requests.packages.urllib3.disable_warnings()

proxies = {
    #"http": "https://localhost:8087",
    #'http': 'socks5://localhost:7070'
}


##########################################################################
class Worker(Thread):
    # thread pool, must python 2.7 up
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
    # thread pool
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

def DownloadPBF(url, savefile):
    # 下载文件
    mutex.acquire()
    print savefile
    mutex.release()
    #
    if (os.path.exists(savefile)): return
    response = requests.get(url, proxies=proxies, stream=True)
    data = response.raw.read()
    f = open(savefile, 'wb')
    f.write(data)
    f.close()
    


if __name__ == '__main__':
    #
    print '[==DoDo==]'
    print 'Tile Maker.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    
    # init
    maxThreads = 16                         # the num of thread
    outpath = './out/'                      # output path
    fontname = 'DIN Offc Pro Regular,Arial Unicode MS Regular'        # map name
    fontpath = outpath + fontname + '/'


    
    
    # make output dir
    if (os.path.exists(outpath)==False): os.makedirs(outpath)
    if (os.path.exists(fontpath)==False): os.makedirs(fontpath)

    wp = WorkerPool(maxThreads)
    
    for n in range(0, 65535, 256):
        accesstoken = 'pk.eyJ1IjoiYWRvZG8xIiwiYSI6ImNqMHN3ZGxkMTA1OHEzMm81cDFuY29vMHQifQ.XVflxoyK_WveMbKlGW5Jhg'
        url = 'https://api.mapbox.com/fonts/v1/mapbox/%s/%d-%d.pbf?access_token=%s' % (fontname, n, n+255, accesstoken)
        savefile = '%s%d-%d.pbf' % (fontpath, n, n+255)
        wp.add_job(DownloadPBF, url, savefile)

    wp.wait_for_complete()
    
        
    print 'Finish'
    

    
