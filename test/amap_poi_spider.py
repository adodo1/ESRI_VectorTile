#!/usr/bin/env python
# encoding: utf-8

import os, sys, json, requests, time, logging, socket, math, sqlite3
import threading, Queue
from threading import Thread


mutex = threading.Lock()                                    # thread lock !
requests.packages.urllib3.disable_warnings()                # 
logging.getLogger("requests").setLevel(logging.WARNING)     #
logging.getLogger("urllib3").setLevel(logging.WARNING)      #

socket.setdefaulttimeout(15)    # 超时时间15秒
MAX_THREADS = 16                # 最大线程数


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

class Spider:
    # 高德POI爬虫
    def __init__(self, conn):
        # conn 数据库连接
        self.POI_URL = 'http://lbs.amap.com/dev/api'    # 获取POI列表
        self._conn = conn           # 数据库连接


    def GetData(self, params):
        # 获取数据
        # http://lbs.amap.com/dev/api?keywords=银行&types=160000&city=柳州&children=1&offset=20&page=0&extensions=all
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            #'Accept': 'application/json, text/javascript, */*; q=0.01',
            #'Origin': 'http://lbs.amap.com',
            #'Referer': 'http://lbs.amap.com/api/webservice/guide/api/search/',
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
        try:
            r = requests.post(self.POI_URL, params=params, headers=headers, data=data)
            data = json.loads(r.content)
            if (data.has_key('code')):
                logging.error('get data err: %s' % params)
                return {'status': '0'}
            else: return data
        except Exception, ex:
            raise ex
        
    def GetJson(self, params):
        # 获取数据尝试3次
        try:
            return self.GetData(params)
        except:
            try:
                return self.GetData(params)
            except:
                try:
                    return self.GetData(params)
                except Exception, ex:
                    logging.error('%s' % s)
                    return None

    def GetTotal(self, params):
        # 获得结果总数
        data = self.GetJson(params)
        if (int(data['status']) != 1): return 0
        else: return int(data['count'])

    def AddTasks(self, params, tasks):
        # 添加任务到全局的任务列表
        # 查询总数
        offset = 20
        total = self.GetTotal(params)
        logging.info('types: %s  total: %d' % (params['types'], total))
        if (total == 0): return
        # 放入任务列表中
        mutex.acquire()
        for n in range(0, int(math.ceil(total // offset))):
            #params['offset'] = offset
            #params['page'] = n + 1
            #params['extensions'] = 'all'
            task = {
                'keywords': params['keywords'],
                'types': params['types'],
                'city': params['city'],
                'children': params['city'],
                'offset': offset,
                'page': n+1,
                'extensions': 'all'
            }
            
            # 加入列表
            tasks.append(task)
        mutex.release()

    def TaskThread(self, params):
        # 任务线程
        conn = self._conn

        # 查询数据库里是否有记录
        total = 0
        data = self.GetJson(params)
        if (int(data['status']) != 1): total = 0
        else: total = int(data['count'])

        
        mutex.acquire()
        
        global success_num
        global tasks_count
        success_num += 1
        logging.info('task [%d/%d]: CODE: %s - PAGE: %d' % (success_num, tasks_count, params['types'], params['page']))
        if (data != None):
            # 插入记录到数据库
            args = (params['keywords'],
                    params['types'],
                    params['city'],
                    params['offset'],
                    params['page'],
                    total,
                    json.dumps(data),
                    int(time.time()))
            
            # 插入记录
            cursor = conn.cursor()
            cursor.execute('insert into POIDATA values(?,?,?,?,?,?,?,?)', args)
            if (success_num % 1000 == 0):
                conn.commit()
            
        mutex.release()

def InitLOG(fname):
    # 初始化日志
    # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=fname,
                filemode='a')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(message)s', '%H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def InitDB(conn):
    # 初始化数据库
    cu = conn.cursor()

    # 创建POIDATA表
    cu.execute(
        """create table if not exists POIDATA(
               keywords varchar(20),    -- 关键字
               types varchar(20),       -- 分类ID
               city varchar(20),        -- 城市ID
               
               offset int,              -- 每页数量
               page int,                -- 页数
               total int,               -- 结果总数
               context text,            -- json内容
               time number)             -- 时间戳
        """)

success_num = 0
tasks_count = 0

if __name__=='__main__':
    print '[==DoDo==]'
    print 'get amap pois.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 初始化
    if (os.path.exists('./output')==False):
        os.mkdir('./output')
    logfile = './output/amap_poi.log'
    dbfile = './output/amap_poi.db'

    # 初始化
    conn = sqlite3.connect(dbfile, check_same_thread = False)
    InitLOG(logfile)
    InitDB(conn)
    spider = Spider(conn)
    
    # 读取所有的types
    text = open('types.txt', 'r').read()
    text = text.strip()
    text.replace('\r', '')
    typeslst = text.split('\n')



    # 任务计划
    tasks = []

    # 循环所有类别 添加任务
    wp = WorkerPool(MAX_THREADS)
    for types in typeslst:
        params = {
            'keywords': '',
            'types': types,
            'city': u'柳州',
            'children': 1,
            'offset': 1,
            'page': 1,
            'extensions': 'base'
        }
        wp.add_job(spider.AddTasks, params, tasks)
    wp.wait_for_complete()
    # 保存任务列表
    f = open('tasks.json', 'w')
    f.write(json.dumps(tasks))
    f.close()

    # 开始任务
    tasks_count = len(tasks)
    print 'task count:', tasks_count
    wp = WorkerPool(MAX_THREADS)
    for n in range(0, tasks_count):
        params = tasks[n]
        wp.add_job(spider.TaskThread, params)
    #
    wp.wait_for_complete()

    
    conn.commit()
    conn.close()
    logging.shutdown()
    print 'OK.'
    






