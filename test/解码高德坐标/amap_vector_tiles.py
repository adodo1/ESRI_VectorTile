#!/usr/bin/env python
# encoding: utf-8
import os, sys, math 


'''
    function l(tilecoors, outcoorsarr, tilesize2048) {
        var pixelX = 0
          , pixelY = 0
          , pixelX = 256 * outcoorsarr.x
          , pixelY = 256 * outcoorsarr.y;
          
        outcoorsarr = [];
        for (var outtilecoorslist = [], outcoorslist = [], k01 = Math.pow(2, 2), coorindex = 0, m01 = tilecoors.length; coorindex < m01; coorindex += 2) {
            var mercatorX = (pixelX + tilecoors[coorindex]) * tilesize2048 - 53109887 * k01
              , mercatorY = (pixelY + tilecoors[coorindex + 1]) * tilesize2048 - 26262068 * k01
              , outcoorslen = outcoorslist.length;

            if (0 === outcoorsarr.length || mercatorX !== outcoorslist[outcoorslen - 2] || mercatorY !== outcoorslist[outcoorslen - 1])
                1 < outcoorsarr.length ? mercatorX === outcoorslist[outcoorslen - 2] && mercatorX === outcoorslist[outcoorslen - 4] ? (outcoorslist[outcoorslen - 1] = mercatorY,
                outcoorsarr[outcoorsarr.length - 1][1] = mercatorY,
                outtilecoorslist[outcoorsarr.length - 1][1] = tilecoors[coorindex + 1]) : mercatorY === outcoorslist[outcoorslen - 1] && mercatorY === outcoorslist[outcoorslen - 3] ? (outcoorslist[outcoorslen - 2] = mercatorX,
                outcoorsarr[outcoorsarr.length - 1][0] = mercatorX,
                outtilecoorslist[outcoorsarr.length - 1][0] = tilecoors[coorindex]) : (outcoorslist.push(mercatorX),
                outcoorslist.push(mercatorY),
                outcoorsarr.push([mercatorX, mercatorY]),
                outtilecoorslist.push([tilecoors[coorindex], tilecoors[coorindex + 1]])) : (outcoorslist.push(mercatorX),
                outcoorslist.push(mercatorY),
                outcoorsarr.push([mercatorX, mercatorY]),
                outtilecoorslist.push([tilecoors[coorindex], tilecoors[coorindex + 1]]))
        }
        return [outcoorslist, outcoorsarr, outtilecoorslist]
    }
'''


def TileCoorsToMercator(tilecoors, tileX, tileY, tileZ, size):
    # 瓦片相对坐标转墨卡托坐标
    pixelX = 256 * tileX
    pixelY = 256 * tileY

    result = []
    times = math.pow(2, 2)

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
                


if __name__ == '__main__':
    print '[==DoDo==]'
    print 'amap voter tiles.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 高德地图瓦片解析
    r = StrToCoors('RQfARQfgREfgRRfUREfD')
    print r
    print len(r)

    # [0, 234, 0, 256, 2, 256, 3, 249, 2, 236]
    # {z: 9, x: 396, y: 224, N: 2048}
    # 2048

    # [99, 88, 99, 89, 100, 89, 100, 88]
    # {z: 10, x: 817, y: 439, N: 1024}
    #
    # [[1833476.0, 10123056.0], [1833476.0, 10124080.0], [1834500.0, 10124080.0], [1834500.0, 10123056.0]]
    

    r = [107, 189, 107, 190, 108, 190, 108, 189]
    r = TileCoorsToMercator(r, 817, 439, 10, 1024)
    print r
    
    # [-4821500, 12871472, -4821500, 12916528, -4817404, 12916528, -4815356, 12902192, -4817404, 12875568]

    #0:[-4821500, 12871472]
    #1:[-4821500, 12916528]
    #2:[-4817404, 12916528]
    #3:[-4815356, 12902192]
    #4:[-4817404, 12875568]

    #0[0, 234]
    #1[0, 256]
    #2[2, 256]
    #3[3, 249]
    #4[2, 236]











    
