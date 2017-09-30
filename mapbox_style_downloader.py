#!/usr/bin/env python
# encoding: utf-8

import os, sys, math, requests, time, json, socket

socket.setdefaulttimeout(20)    # outtime set 20s
proxies = {
    "http": "https://localhost:8087"
    }

def GetHtml(url):
    # 获取文本
    try:
        response = requests.get(url, proxies=proxies, stream=True)
        data = response.content
        return data
    except Exception, ex:
        raise ex

def GetRaw(url):
    # 获取原始数据
    try:
        response = requests.get(url, proxies=proxies, stream=True)
        data = response.raw.read()
        return data
    except Exception, ex:
        raise ex
    
if __name__ == '__main__':
    #
    print '[==DoDo==]'
    print 'Tile Downloader (mapbox).'
    print 'Encode: %s' %  sys.getdefaultencoding()
    requests.packages.urllib3.disable_warnings()

    # 只负责MAPBOX样式下载
    
    # 初始化
    style_name = 'mapbox://styles/mapbox/streets-v9'
    accessToken = 'pk.eyJ1IjoiYWRvZG8xIiwiYSI6ImNqMHN3ZGxkMTA1OHEzMm81cDFuY29vMHQifQ.XVflxoyK_WveMbKlGW5Jhg'

    outpath = './out/'                      # output path
    mapname = 'MAP'                         # map name


    # 目录结构 参照ESRI目录组织
    # MAP/
    #     root.json         # 元数据信息
    #
    #     resources/        # 资源目录
    #         fonts/        # 字体文件夹
    #         sprites/      # CSS样式和图片
    #         styles/       # 样式文件夹
    #     tile/             # 瓦片数据
    #
    #     task.txt          # 任务元数据
    #

    # 创建目录结构
    map_path = outpath + mapname + '/'
    metadata_file = map_path + 'root.json'
    task_file = map_path + 'task.txt'
    resources_path = map_path + 'resources/'
    fonts_path = resources_path + 'fonts/'
    sprites_path = resources_path + 'sprites/'
    styles_path = resources_path + 'styles/'
    styles_file = styles_path + 'root.json'
    tile_path = map_path + 'tile/'
    

    if (os.path.exists(map_path)==False): os.makedirs(map_path)
    if (os.path.exists(resources_path)==False): os.makedirs(resources_path)
    if (os.path.exists(fonts_path)==False): os.makedirs(fonts_path)
    if (os.path.exists(sprites_path)==False): os.makedirs(sprites_path)
    if (os.path.exists(styles_path)==False): os.makedirs(styles_path)
    if (os.path.exists(tile_path)==False): os.makedirs(tile_path)


    # 样式元数据
    # https://api.mapbox.com/styles/v1/mapbox/streets-v9?access_token=pk.eyJ1IjoiYWRvZG8xIiwiYSI6ImNqMHN3ZGxkMTA1OHEzMm81cDFuY29vMHQifQ.XVflxoyK_WveMbKlGW5Jhg
    if (os.path.exists(styles_file) == False):
        styles_url = 'https://api.mapbox.com/styles/v1/{0}?access_token={1}'.format(style_name[16:], accessToken)
        print 'style file: %s' % styles_url
        data = GetHtml(styles_url)
        f = open(styles_file, 'wb')
        f.write(data)
        f.close()
        print 'len: %d' % len(data)
    else:
        print 'style file: %s' % styles_file
        f = open(styles_file, 'rb')
        data = f.read()
        f.close()
        print 'len: %d' % len(data)

    # 下载sources
    # https://api.mapbox.com/v4/mapbox.mapbox-terrain-v2,mapbox.mapbox-streets-v7.json?secure&access_token=pk.eyJ1IjoiYWRvZG8xIiwiYSI6ImNqMHN3ZGxkMTA1OHEzMm81cDFuY29vMHQifQ.XVflxoyK_WveMbKlGW5Jhg
    styles_json = json.loads(data)
    sources = styles_json['sources']
    for source in sources:
        if (sources[source]['type'].lower() == 'vector'):
            source_metadatafile = '{0}{1}.json'.format(tile_path, source)
            if (os.path.exists(source_metadatafile) == False):
                vector_url = sources[source]['url']
                print 'source: %s' % source
                # 构造瓦片URL
                vector_url = 'https://api.mapbox.com/v4/{0}.json?secure&access_token={1}'.format(vector_url[9:], accessToken)
                print 'url: %s' % vector_url
                data = GetHtml(vector_url)
                f = open(source_metadatafile, 'wb')
                f.write(data)
                f.close()
                print 'len: %d' % len(data)
            else:
                f = open(source_metadatafile, 'rb')
                data = f.read()
                f.close()
            # 
            
            
            















    
