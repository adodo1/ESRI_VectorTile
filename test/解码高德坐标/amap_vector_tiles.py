#!/usr/bin/env python
# encoding: utf-8
import os, sys, math 


'''
    function l(tilecoors, xyz_tilesize, tilesize2048) {
        var d01 = 0
          , f01 = 0
          , d01 = 256 * xyz_tilesize.x
          , f01 = 256 * xyz_tilesize.y;
          
        xyz_tilesize = [];
        for (var g01 = [], h01 = [], k01 = Math.pow(2, 2), l01 = 0, m01 = tilecoors.length; l01 < m01; l01 += 2) {
            var n01 = (d01 + tilecoors[l01]) * tilesize2048 - 53109887 * k01
              , p01 = (f01 + tilecoors[l01 + 1]) * tilesize2048 - 26262068 * k01
              , q01 = h01.length;

            if (0 === xyz_tilesize.length || n01 !== h01[q01 - 2] || p01 !== h01[q01 - 1])
                1 < xyz_tilesize.length ? n01 === h01[q01 - 2] && n01 === h01[q01 - 4] ? (h01[q01 - 1] = p01,
                xyz_tilesize[xyz_tilesize.length - 1][1] = p01,
                g01[xyz_tilesize.length - 1][1] = tilecoors[l01 + 1]) : p01 === h01[q01 - 1] && p01 === h01[q01 - 3] ? (h01[q01 - 2] = n01,
                xyz_tilesize[xyz_tilesize.length - 1][0] = n01,
                g01[xyz_tilesize.length - 1][0] = tilecoors[l01]) : (h01.push(n01),
                h01.push(p01),
                xyz_tilesize.push([n01, p01]),
                g01.push([tilecoors[l01], tilecoors[l01 + 1]])) : (h01.push(n01),
                h01.push(p01),
                xyz_tilesize.push([n01, p01]),
                g01.push([tilecoors[l01], tilecoors[l01 + 1]]))
        }
        return [h01, xyz_tilesize, g01]
    }
'''


def TileCoorsToMercator(tilecoors, tileX, tileY, tileZ, size):
    # 瓦片相对坐标转墨卡托坐标
    d01 = 256 * tileX
    f01 = 256 * tileY

    xyz_tilesize = []
    g01 = []
    h01 = []
    k01 = math.pow(2, 2)
    m01 = len(tilecoors)

    for l01 in range(0, m01, 2):
        n01 = (d01 + tilecoors[l01]) * size - 53109887 * k01
        p01 = (f01 + tilecoors[l01 + 1]) * size - 26262068 * k01
        q01 = len(h01)

        print n01, p01, q01

        if (0 == len(xyz_tilesize) or n01 != h01[q01 - 2] or p01 != h01[q01 - 1]):
            print 'aaaaaa'
        
    
    


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

    TileCoorsToMercator(r, 396, 224, 9, 2048)
    
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











    
