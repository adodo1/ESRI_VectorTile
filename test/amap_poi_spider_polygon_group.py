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
        self._conn = conn               # 数据库连接

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
            'type': 'place/polygon',
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

    def GetCoorsList(self, minlng, minlat, maxlng, maxlat):
        # 坐标分组 1块分4块
        midlat = (maxlat + minlat) / 2.0
        midlng = (maxlng + minlng) / 2.0
        coors = []
        #coorstr = '%.6f,%.6f|%.6f,%.6f' % (minlng, minlat, midlng, midlat)
        #coors.append(coorstr)
        #coorstr = '%.6f,%.6f|%.6f,%.6f' % (minlng, midlat, midlng, maxlat)
        #coors.append(coorstr)
        #coorstr = '%.6f,%.6f|%.6f,%.6f' % (midlng, minlat, maxlng, midlat)
        #coors.append(coorstr)
        #coorstr = '%.6f,%.6f|%.6f,%.6f' % (midlng, midlat, maxlng, maxlat)
        #coors.append(coorstr)
        coors.append([minlng, minlat, midlng, midlat])
        coors.append([minlng, midlat, midlng, maxlat])
        coors.append([midlng, minlat, maxlng, midlat])
        coors.append([midlng, midlat, maxlng, maxlat])
        return coors

    def AddTasks(self, params, tasks, collection):
        # 添加任务到全局的任务列表
        global network_err
        if (network_err): return
        
        # 查询总数
        offset = 20
        data = self.GetJson(params)
        # 高德地图网络和谐代码
        if (int(data['status']) == 1111):
            network_err = True
            return
        if (int(data['status']) != 1): total = 0
        else: total = int(data['count'])
            
        logging.info('types: %s coors: %s  total: %d -- %d' % (params['types'], params['polygon'], total, len(collection)))
        if (total == 0): return
        # 放入任务列表中
        mutex.acquire()
        global success_num
        global tasks_count

        success_num += 1
        if (success_num % 100 == 0):
            logging.info('>>>>>>>>>>>>> %d / %d' % (success_num, tasks_count))

        # 解析出坐标点
        coors = params['polygon'].split('|')
        minlng = float(coors[0].split(',')[0])
        minlat = float(coors[0].split(',')[1])
        maxlng = float(coors[1].split(',')[0])
        maxlat = float(coors[1].split(',')[1])
        # 3种情
        # 1. 总数小于 800 直接加入任务组
        # 2. 总数大于等于 800 按照范围进行重新分组
        # 3. 当范围已经缩小到最小 但是结果还是大于800个 不再进行重新分组
        if (total < 800):
            # 直接加入任务组
            for n in range(0, int(math.ceil(total // offset))):
                task = {
                    'polygon': params['polygon'],
                    'keywords': params['keywords'],
                    'types': params['types'],
                    'offset': offset,
                    'page': n+1,
                    'extensions': 'all'
                }
                # 加入列表
                tasks.append(task)
        elif (maxlng - minlng < 0.000001) and (maxlat - minlat < 0.000001):
            # 因为高德限制小数点后6位 如果在这么小的范围里还是多余800个就不再分组
            logging.error('types: %s coors: %s  total: %d more than 800 -- %d' % (params['types'], params['polygon'], total, len(collection)))
            for n in range(0, int(math.ceil(total // offset))):
                task = {
                    'polygon': params['polygon'],
                    'keywords': params['keywords'],
                    'types': params['types'],
                    'offset': offset,
                    'page': n+1,
                    'extensions': 'all'
                }
                # 加入列表
                tasks.append(task)
        else:
            # 需要重新分组
            coors = self.GetCoorsList(minlng, minlat, maxlng, maxlat)
            for coor in coors:
                collection.append([params['types'], coor])
                
        mutex.release()


    def TaskThread(self, params):
        # 任务线程
        global network_err
        if (network_err): return
        # 
        conn = self._conn
        # 查询数据库里是否有记录
        total = 0
        data = self.GetJson(params)
        if (int(data['status']) == 1111):
            network_err = True
            return
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
                    'none',
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
network_err = False     # 网络故障

if __name__=='__main__':
    print '[==DoDo==]'
    print 'get amap pois by polygon.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    f = open('poitasks.json', 'r')
    text = f.read()
    f.close()
    poitasks = json.loads(text)
    for poitask in poitasks:
        tid = poitask
        coors = poitasks[tid]
        
        # 初始化
        if (os.path.exists('./output')==False):
            os.mkdir('./output')
        logfile = './output/{0}.log'.format(tid)
        dbfile = './output/{0}.db'.format(tid)
        taskfile = './output/{0}_tasks.json'.format(tid)
        regroupfile = './output/{0}_regroup.json'.format(tid)
        missionfile = './output/{0}_mission.json'.format(tid)
        finishfile = './output/{0}_finish.lock'.format(tid)
        
        if (os.path.exists(finishfile)): continue
        
        # 经纬度范围
        top_lat = coors[0]
        left_lng = coors[1]
        bottom_lat = coors[2]
        right_lng = coors[3]

        print '@@@@@@@@@@@@@@@@@@@@@@@@@'
        print 'TASK:', tid
        print 'COORS:', coors
        print '@@@@@@@@@@@@@@@@@@@@@@@@@'
        
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



        tasks = []          # 所有任务
        regroup = []        # 重新分组 如果数组不为空就一直循环下去

        # 判断是否存在任务文件 如果存在从中断的任务开始执行
        if (os.path.exists(taskfile)):
            f = open(taskfile, 'r')
            tasks = json.loads(f.read())
            f.close()
        if (os.path.exists(regroupfile)):
            f = open(regroupfile, 'r')
            regroup = json.loads(f.read())
            f.close()
            
        # 如果没有中断的任务
        if (len(regroup) == 0):
            for types in typeslst:
                regroup.append([types, [left_lng, bottom_lat, right_lng, top_lat]])

        hasdo = set()

        while True:
            print '########################################################'
            print '########################################################'
            print '########################################################'
            print '########################################################'
            if (len(regroup) == 0): break
            # 循环所有类别 添加任务
            collection = []     # 用来收集新任务
            wp = WorkerPool(MAX_THREADS)

            for group in regroup:
                types = group[0]
                coors = tuple(group[1])
                # 程序还有缺陷 已经请求过的数据还要重复请求 偷个懒
                uuids = '%s:%s' % (types, coors)
                if (uuids in hasdo): continue
                else: hasdo.add(uuids)
                #
                params = {
                    'polygon': '%.6f,%.6f|%.6f,%.6f' % coors,
                    'keywords': '',
                    'types': types,
                    'offset': 1,
                    'page': 1,
                    'extensions': 'base'
                }
                wp.add_job(spider.AddTasks, params, tasks, collection)
            wp.wait_for_complete()
            # 如果发生网络故障跳出
            if (network_err): break
            # 收集到的新组重新循环
            regroup = collection


        # 网络故障处理
        # 如果请求被高德和谐 会产生1111错误
        # 保存当前已搜集的任务列表
        # 保存当前未完成的重分组列表
        if (network_err):
            f = open(taskfile, 'w')
            f.write(json.dumps(tasks))
            f.close()
            f = open(regroupfile, 'w')
            f.write(json.dumps(regroup))
            f.close()
            # 抛出异常中断任务
            raise Exception()
            
        
        print '==============================================='
        
        # 保存任务列表
        f = open(missionfile, 'w')
        f.write(json.dumps(tasks))
        f.close()

        # 开始任务
        success_num = 0
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
        f = open(finishfile, 'w')
        f.write('ok')
        f.close()
        print 'OK.'







