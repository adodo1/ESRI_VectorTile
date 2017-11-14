#!/usr/bin/env python
# encoding: utf-8

import os, sys, json, time, math, sqlite3


def GetUids(data):
    # 获取所有的uid
    uids = []
    if (int(data['status'])!=1): return uids
    for poi in data['pois']:
        uid = poi['id']
        uids.append(uid)
    return uids

if __name__=='__main__':
    print '[==DoDo==]'
    print 'decode amap pois.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 高德地图POI解码
    # 初始化
    dbfile = './output/amap_poi.db'
    conn = sqlite3.connect(dbfile, check_same_thread = False)

    result = []
    cursor = conn.cursor()
    sql = 'select context from POIDATA'
    cursor.execute(sql)
    record = cursor.fetchall()
    for row in record:
        context = row[0]
        data = json.loads(context)
        uids = GetUids(data)
        result.extend(uids)
    # 数据去重
    s = set(result)
    result = [i for i in s]
    
    print 'OK.'
    






