#!/usr/bin/env python
# encoding: utf-8

import os, sys, json, time, math, sqlite3

PI              = 3.14159265358979323846                    # PI
EARTH_RADIUS    = 6378245.0                                 # 地球半径
EE              = 0.00669342162296594323                    # 扁率
X_PI            = 3.14159265358979324 * 3000.0 / 180.0      # 



class MarsCoor:
    # 火星坐标
    def OutOfChina(self, lat, lng):
        # 坐标是否在中国外
        if (lng < 72.004 or lng > 137.8347):
            return True
        if (lat < 0.8293 or lat > 55.8271):
            return True
        return False

    def TransformLat(self, x, y):
        # 纬度转换
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
        return ret

    def TransformLng(self, x, y):
        # 经度转换
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
        return ret

    def GPS2Mars(self, wglat, wglng):
        # 地球坐标转换为火星坐标
        # wglat WGS纬度
        # wglng WGS经度
        # 返回近似火星坐标系
        if (self.OutOfChina(wglat, wglng)):
            return wglat, wglng
        dlat = self.TransformLat(wglng - 105.0, wglat - 35.0)
        dlng = self.TransformLng(wglng - 105.0, wglat - 35.0)
        radlat = wglat / 180.0 * PI
        magic = math.sin(radlat)
        magic = 1 - EE * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((EARTH_RADIUS * (1 - EE)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (EARTH_RADIUS / sqrtmagic * math.cos(radlat) * PI)
        mglat = wglat + dlat
        mglng = wglng + dlng
        return mglat, mglng

    def Mars2GPS(self, gclat, gclng):
        # 采用二分法 火星坐标反算地球坐标
        # gclat 火星坐标纬度
        # gclng 火星坐标经度
        initDelta = 0.01
        threshold = 0.000000001
        dlat = initDelta
        dlng = initDelta
        mlat = gclat - dlat
        mlng = gclng - dlng
        plat = gclat + dlat
        plng = gclng + dlng
        wgslat = 0
        wgslng = 0
        i = 0
        while (True):
            wgslat = (mlat + plat) / 2.0
            wgslng = (mlng + plng) / 2.0
            tmplat, tmplng = self.GPS2Mars(wgslat, wgslng)
            dlat = tmplat - gclat
            dlng = tmplng - gclng

            if ((abs(dlat)<threshold) and (abs(dlng)<threshold)):
                break
            if (dlat > 0): plat = wgslat
            else: mlat = wgslat
            if (dlng > 0): plng = wgslng
            else: mlng = wgslng

            i += 1
            if (i>10000): break
        return wgslat, wgslng


def GetData(data):
    # 获取所有的uid
    marsCoor = MarsCoor()
    result = []
    if (int(data['status'])!=1): return result
    for poi in data['pois']:
        uid = u'%s' % poi['id']
        tag = u'%s' % poi['tag']
        name = u'%s' % poi['name']
        dtype = u'%s' % poi['type']
        typecode = u'%s' % poi['typecode']
        address = u'%s' % poi['address']
        tel = u'%s' % poi['tel']
        pcode = u'%s' % poi['pcode']
        pname = u'%s' % poi['pname']
        citycode = u'%s' % poi['citycode']
        cityname = u'%s' % poi['cityname']
        adcode = u'%s' % poi['adcode']
        adname = u'%s' % poi['adname']
        business_area = u'%s' % poi['business_area']
        
        # 火星 转 WGS84
        location = poi['location']
        marlng, marlat = location.split(',')
        marlng = float(marlng)
        marlat = float(marlat)
        lat, lng = marsCoor.Mars2GPS(marlat, marlng)
        #
        result.append((uid, tag, name, dtype, typecode, address, tel, pcode, pname, citycode, cityname, adcode, adname, business_area, marlat, marlng, lat, lng))
    return result

def InitDB(conn):
    # 初始化数据库
    cu = conn.cursor()
    # 创建POIS表
    cu.execute(
        """create table if not exists POIS(
               id varchar(20),              -- 
               tag text,                    -- 
               name varchar(50),            -- 
               dtype varchar(50),           -- 
               typecode varchar(20),        -- 
               address varchar(100),        -- 
               tel varchar(40),             -- 
               pcode varchar(20),           -- 
               pname varchar(20),           -- 
               citycode varchar(20),        -- 
               cityname varchar(20),        -- 
               adcode varchar(20),          -- 
               adname varchar(20),          -- 
               business_area varchar(20),   -- 

               marlat number,               -- 火星纬度
               marlng number,               -- 火星经度
               lat number,                  -- 纬度
               lng number                   -- 经度
               )
        """)

if __name__=='__main__':
    print '[==DoDo==]'
    print 'decode amap pois.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 高德地图POI解码
    # 初始化
    dbfile = './output/amap_poi_polygon.db'
    conn = sqlite3.connect(dbfile, check_same_thread = False)
    # 创建数据库
    InitDB(conn)

    result = []
    cursor = conn.cursor()
    sql = u'select context from POIDATA'
    cursor.execute(sql)

    num = 0
    row = cursor.fetchone()
    while row != None:
        num += 1
        if (num % 1000==0): print num
        
        context = row[0]
        try:
            data = json.loads(context)
        except Exception, ex:
            f = open('_error.txt', 'a')
            f.write(context)
            f.write('\n')
            f.close()
            continue
        udatas = GetData(data)
        # 保存
        for udata in udatas:
            result.append(udata)
        #
        row = cursor.fetchone()
        

    print 'total: %d' % len(result)
    # 插入数据库
    cursor = conn.cursor()
    for data in result:
        cursor.execute('insert into POIS values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()
        
    '''
    record = cursor.fetchall()
    for row in record:
        context = row[0]
        data = json.loads(context)
        uids = GetUids(data)
        result.extend(uids)
    '''
    # 数据去重
    s = set(result)
    result = [i for i in s]
    
    print 'OK.'
    






