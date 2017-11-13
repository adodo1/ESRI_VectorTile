#!/usr/bin/env python
# encoding: utf-8

import os, sys, json, requests


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
    print num, data['count'], data['info'], data['pois'][0]['name']


if __name__=='__main__':
    print '[==DoDo==]'
    print 'get amap pois.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    for i in range(1, 45):
        test(i)

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









