#!/usr/bin/env python
# encoding: utf-8
import os, sys, math 

# 新版的高德地图使用websocket获取瓦片
# 旧版的使用rest请求
# Host: vdata.amap.com
# Sec-WebSocket-Version: 13
# ws://vdata.amap.com/


def TileCoorsToMercator(tilecoors, tileX, tileY, tileZ):
    # 瓦片相对坐标转墨卡托坐标 - -; 并不是墨卡托坐标
    # size计算方法 Math.pow(2, 20 - h)
    pixelX = 256 * tileX
    pixelY = 256 * tileY

    result = []
    times = math.pow(2, 2)
    size = math.pow(2, 20 - tileZ)

    for coorindex in range(0, len(tilecoors), 2):
        mercatorX = (pixelX + tilecoors[coorindex]) * size - 53109887 * times
        mercatorY = (pixelY + tilecoors[coorindex + 1]) * size - 26262068 * times
        result.append([mercatorX, mercatorY])
    return result
    
def StrToCoors(cstr):
    # 坐标字符串转瓦片相对坐标
    result = []
    num = None
    for ch in cstr:
        index = 'ASDFGHJKLQWERTYUIO!sdfghjkl'.find(ch)
        if (num == None): num = 27 * index
        else:
            result.append(num + index - 333)
            num = None
    return result

def CalTileXY(tileX, tileY, tileZ):
    # 计算高德瓦片XY
    # 例如: http://vdata.amap.com/tiles?mapType=normal&v=2&style=4&rd=1&flds=region,building,road&t=12,65,0&lv=12
    # 得到的实际瓦片为 12-64-1
    size = int(math.pow(2, int((tileZ + 1) / 2)))
    x = size * (tileX / size) + tileY % size
    y = tileX % size + size * (tileY / size)
    return x, y
    

if __name__ == '__main__':
    print '[==DoDo==]'
    print 'amap voter tiles.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    cstr = '''
           '''

    #11,600,233
    print CalTileXY(105041,56729,17)

    # 高德地图瓦片解析
    r = StrToCoors(cstr.strip())
    print r
    print len(r)

    # [0, 234, 0, 256, 2, 256, 3, 249, 2, 236]
    # {z: 9, x: 396, y: 224, N: 2048}
    # 2048

    # [99, 88, 99, 89, 100, 89, 100, 88]
    # {z: 10, x: 817, y: 439, N: 1024}
    #
    # [[1833476.0, 10123056.0], [1833476.0, 10124080.0], [1834500.0, 10124080.0], [1834500.0, 10123056.0]]
    r = TileCoorsToMercator(r, 3292, 1762, 11)
    print r

    for a in r:
        print a[0], a[1]












    
