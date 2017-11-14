#!/usr/bin/env python
# encoding: utf-8

import os, sys, re, math, json, shapefile
import zlib, gzip, StringIO

class GMap:
    # GMap class
    def __init__(self):
        self.MinLatitude = -85.05112878     # min latitude
        self.MaxLatitude = 85.05112878      # max latitude
        self.MinLongitude = -180            # min longitude
        self.MaxLongitude = 180             # max longitude
        self.TileSizeWidth = 256            # tile width
        self.TileSizeHeight = 256           # tile height
        self.Dpi = 96.0                     # tile dpi

    def GetTileMatrixMinXY(self, zoom):
        # tile min xy
        return 0, 0

    def GetTileMatrixMaxXY(self, zoom):
        # tile max xy
        xy = (1 << zoom)
        return xy - 1, xy - 1

    def GetTileMatrixSizePixel(self, zoom):
        # tile full pixel size
        sMin = self.GetTileMatrixMinXY(zoom)
        sMax = self.GetTileMatrixMaxXY(zoom)
        width = (sMax[0] - sMin[0] + 1) * self.TileSizeWidth
        height = (sMax[1] - sMin[1] + 1) * self.TileSizeHeight
        return width, height

    def GetMAPScale(self, zoom, lat=0):
        # http://wenku.baidu.com/link?url=I-RdILcOskWLkqYvLetcFFr7JiURwY4WxfOlKEe8gwkJp_WS6O9H7KNOz0YTBu5Fo8Ff0WcurgeYVPvRY2c2k10805MV-Taj4JXRK4aVqje
        # http://www.360doc.com/content/15/0319/13/9009195_456410364.shtml
        # http://wenku.baidu.com/view/359c88d6b14e852458fb5754.html
        # http://www.cnblogs.com/beniao/archive/2010/04/18/1714544.html
        # http://gis.stackexchange.com/questions/7430/what-ratio-scales-do-google-maps-zoom-levels-correspond-to < useful
        #
        #level     dis       px    map_dis   dpi      scale      ground_resolution
        #level2    5000km    70    2.47cm    72dpi    2b : 1     71km    
        #level3    2000km    55    1.94cm    72dpi    1b : 1     36km    36363.63636363636
        #level4    2000km    115   4.06cm    72dpi    5kw : 1    17km    17391.30434782609
        #level5    1000km    115   4.06cm    72dpi    2.5kw : 1  9km     8695.652173913043
        #level6    500km     115   4.06cm    72dpi    1.2kw : 1  4km     4347.826086956522
        #level7    200km     91    3.21cm    72dpi    6hw : 1    2km     2197.802197802198
        #level8    100km     176   6.21cm    72dpi    160w : 1   568m    568.1818181818182
        #level9    50km      91    3.21cm    72dpi    155w : 1   549m    549.4505494505495
        #level10   20km      72    2.54cm    72dpi    80w : 1    278m    277.7777777777778
        #level11   10km      72    2.54cm    72dpi    40w : 1    139m    138.8888888888889
        #level12   5km       72    2.54cm    72dpi    20w : 1    69m     69.44444444444444
        #level13   2km       57    2.01cm    72dpi    10w : 1    35m     35.0877192982456
        #level14   2km       118   4.16cm    72dpi    5w : 1     17m     16.9491525423729
        #level15   1km       118   4.16cm    72dpi    2.5w : 1   8m      8.4745762711864
        #level16   500m      118   4.16cm    72dpi    1.2w : 1   4m      4.23728813559322
        #level17   200m      93    3.28cm    72dpi    2300 : 1   2.15m   2.150537634408602
        #level18   100m      93    3.28cm    72dpi    3000 : 1   1.07m   1.075268817204301
        #level19   50m       93    3.28cm    72dpi    1500 : 1   0.54m   0.5376344086021505
        #level20   20m       74    2.61cm    72dpi    800 : 1    0.27m   0.2702702702702703

        # ground_resolution = (math.cos(lat * math.pi/180) * 2 * math.pi * 6378137) / (256 * 2^level)
        # map_scale = (math.cos(lat * math.pi/180) * 2 * math.pi * 6378137 * dpi) / (256 * 2^level * 0.0254)
        # ---------------------------------------------------
        # fun 1
        #tile_full_px = self.GetTileMatrixSizePixel(zoom)[0]
        #map_dis = tile_full_px * 0.0254 / self.Dpi          # the dis on map
        #ground_dis = DOMAIN_LEN * 2                         # the dis on ground
        #scale = ground_dis / map_dis
        # ---------------------------------------------------
        # fun 2
        scale = (math.cos(lat * math.pi/180) * (DOMAIN_LEN * 2) * self.Dpi) / (256 * (2 ** zoom) * 0.0254)
        # ---------------------------------------------------
        # fun3
        #scale = 591657550.500000 / (2^(zoom-1))
        return scale
    def GetGroundResolution(self, zoom, lat=0):
        # get resolution
        ground_resolution = (math.cos(lat * math.pi/180) * 2 * math.pi * 6378137) / (256 * (2 ** zoom))
        return ground_resolution

    def FromCoordinateToPixel(self, lat, lng, zoom):
        # gps coordinate to pixel xy  [ gps > pixel xy ]
        # lat: latitude
        # lng: longitude
        # zoom: 0 ~ 19

        # core !!
        # x=(y + 180) / 360
        # y = 0.5 - log((1 + sin(x * 3.1415926 / 180)) / (1 - sin(x * 3.1415926 / 180))) / (4 * pi)
        # y = (1 - (log(tan(x * 3.1415926 / 180) + sec(x * 3.1415926 / 180)) / pi)) / 2
        lat = min(max(lat, self.MinLatitude), self.MaxLatitude)
        lng = min(max(lng, self.MinLongitude), self.MaxLongitude)

        x = (lng + 180) / 360
        y = 0.5 - math.log((1 + math.sin(lat * math.pi / 180)) / (1 - math.sin(lat * math.pi / 180))) / (4 * math.pi)

        mapSizeX, mapSizeY = self.GetTileMatrixSizePixel(zoom)
        pixelX = min(max(x * mapSizeX + 0.5, 0), mapSizeX - 1)
        pixelY = min(max(y * mapSizeY + 0.5, 0), mapSizeY - 1)
        
        return int(pixelX), int(pixelY)

    def FromCoordinateToTileXY(self, lat, lng, zoom):
        # gps coordinate to tile xy  [ gps > tile xy ]
        # lat: latitude
        # lng: longitude
        # zoom: 0 ~ 19
        pixelX, pixelY = self.FromCoordinateToPixel(lat, lng, zoom)
        tileX, tileY = self.FromPixelToTileXY(pixelX, pixelY)
        return tileX, tileY

    def FromPixelToTileXY(self, pixelX, pixelY):
        # full pixel xy to tile xy index
        tileX = int(pixelX / self.TileSizeWidth)
        tileY = int(pixelY / self.TileSizeHeight)
        return tileX, tileY

    def FromPixelToCoordinate(self, pixelX, pixelY, zoom):
        # from pixel xy in tile to gps lat lng
        tile_full_width, tile_full_height = self.GetTileMatrixMaxXY(zoom)
        mapsizex = (tile_full_width + 1) * self.TileSizeWidth
        mapsizey = (tile_full_height + 1) * self.TileSizeHeight

        xx = min(max(pixelX, 0), mapsizex - 1) * 1.0 / mapsizex - 0.5
        yy = 0.5 - (min(max(pixelY, 0), mapsizey - 1) * 1.0 / mapsizey)

        lat = 90 - 360.0 * math.atan(math.exp(-yy * 2 * math.pi)) / math.pi
        lng = 360 * xx
        return lat, lng

# 道路标注
#["16-52737-28200-roadlabel",
#       [
#		[
#			["道", "!kRA", 34, ""],
#			["乡", "!IEO", 50, ""],
#			["3", "!JEL", 44, ""],
#			["1", "OhWk", 40, ""]
#		], "0&12&ff90816f&fffefefd&49", 2, "roads:levelThreeRoad"
#	],
#	[
#		[
#			["Y013", "OfUK", -1, [-12, -12, 24, 24]]
#		], "150&10&ff4a4a4a&00dadada&&50", 3, "roads:guideBoards"
#	]
#]

# POI标注
#["16-52678-28200-poilabel", 
#	[
#		[
#			["中国工商银行", "sROk", "", [-12, -12, 24, 24], "B030401DDE"]
#		], "38&13&ff626467&ffffffff&&1", 1755, 16, "labels:pois"
#	],
#	[
#		[
#			["五菱生活区^河西路2区", "UOIT", [
#					[-32, 12, 65, 13],
#					[-29, 27, 58, 13]
#				],
#				[-12, -12, 24, 24], "B030402N58"
#			]
#		], "91&13&ff626467&fff6f6f4&&0", 1436, 16, "labels:pois"
#	]
#]


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
    # DoDo Y坐标做修正 Y坐标是颠倒的
    #for i in range(0, len(result), 2):
    #    result[i+1] = 256 - result[i+1]
    return result


def EvalLabelTile(text):
    # 解析标注数据
    # 返回结果
    # 
    data = json.loads(text)
    # "16-52674-28200-roadlabel"    当前瓦片XYZ 瓦片图层
    tileinfo = data[0]
    tileinfos = tileinfo.split('-')
    tilez = int(tileinfos[0])
    tilex = int(tileinfos[1])
    tiley = int(tileinfos[2])
    lname = tileinfos[3]
    #print tileinfo
    # 
    features = []
    for i in range(1, len(data)):
        item = data[i]
        if (lname == 'roadlabel') : labels = EvalRoadWaterlabels(item)
        elif (lname == 'poilabel'): labels = EvalPoilabels(item)
        else: raise Exception('{0} is not in labels, roads'.format(lname))
        # 添加注记到要素集合
        for label in labels: features.append(label)

    return {'tilex': tilex,
            'tiley': tiley,
            'tilez': tilez,
            'lname': lname,
            'features': features}


# 注记字段:
# 01. label 文本
# 02. pixx 像素位置X
# 03. pixy 像素位置Y
# 04. angle 文字角度
# 05. icon 图标
# 06. size 文本大小
# 07. fontcolor 文本颜色
# 08. backcolor 背景颜色
# 09. uid 信息ID
# 10. code 分类

def EvalRoadWaterlabels(data):
    # 解析道路标记
    size = len(data)
    if (size != 4): raise Exception('unknow road, water data: %s' % data)
    geos = data[0]
    style = data[1]
    code = data[3]
    #
    styles = style.split('&')
    icon = int(styles[0])
    size = int(styles[1])
    fontcolor = styles[2]
    backcolor = styles[3]
    
    
    uid = ''
    labels = []
    for geo in geos:
        label = geo[0]
        coors = StrToCoors(geo[1])
        angle = int(geo[2])
        pixx = coors[0]
        pixy = coors[1]
        #
        label = {
            'label': label,
            'pixx': pixx,
            'pixy': pixy,
            'angle': angle,
            'icon': icon,
            'size': size,
            'fontcolor': fontcolor,
            'backcolor': backcolor,
            'icontype': '',
            'uid': uid,
            'code': code
                }
        labels.append(label)
    return labels

def EvalPoilabels(data):
    # 解析POI标记
    # 155&13&ff4d4e51&ffffffff&&0
    size = len(data)
    if (size != 5): raise Exception('unknow poi data: %s' % data)
    geos = data[0]
    style = data[1]
    code = data[4]
    #
    styles = style.split('&')
    icon = int(styles[0])
    size = int(styles[1])
    fontcolor = styles[2]
    backcolor = styles[3]
    icontype = int(styles[5])
    
    labels = []
    for geo in geos:
        label = geo[0]
        coors = StrToCoors(geo[1])
        pixx = coors[0]
        pixy = coors[1]
        angle = 0
        uid = geo[len(geo)-1]
        label = {
            'label': label,
            'pixx': pixx,
            'pixy': pixy,
            'angle': angle,
            'icon': icon,
            'size': size,
            'fontcolor': fontcolor,
            'backcolor': backcolor,
            'icontype': icontype,
            'uid': uid,
            'code': code
                }
        labels.append(label)
    return labels


def TileToSHP(text, editor):
    # 把瓦片数据追加到SHP数据里
    gmap = GMap()
    infos = text.split('|')
    for info in infos:
        if (info.startswith('[') == False): continue
        tile = EvalLabelTile(info)
        # 瓦片像素矫正 并往SHP数据里写
        tileX = tile['tilex']
        tileY = tile['tiley']
        tileZ = tile['tilez']
        lname = tile['lname']
        features = tile['features']
        #
        for feature in features:
            #
            label = feature['label'].encode('gbk')
            pixx = feature['pixx']
            pixy = feature['pixy']
            angle = feature['angle']
            icon = feature['icon']
            size = feature['size']
            fontcolor = feature['fontcolor'].encode('gbk')
            backcolor = feature['backcolor'].encode('gbk')
            icontype = feature['icontype']
            uid = feature['uid'].encode('gbk')
            code = feature['code'].encode('gbk')
            # 计算经纬度坐标
            pixelX = tileX * 256 + pixx
            pixelY = tileY * 256 + pixy
            lat, lng = gmap.FromPixelToCoordinate(pixelX, pixelY, tileZ)
            # 写数据到SHP文件
            editor.record(label, angle, icon, size,
                          fontcolor, backcolor, icontype, uid, code)
            editor.point(lng, lat, 0, 0)
            


if __name__=='__main__':
    print '[==DoDo==]'
    print 'amap labels.'
    print 'Encode: %s' %  sys.getdefaultencoding()
    # 解析高德地图的标注数据



    #writer = shapefile.Writer(shapefile.POINT)
    #writer.field('label', 'C', 80)
    #writer.save('labels')
    #editor = shapefile.Editor('labels')
    #editor.record('text')
    #editor.point(1,0,0,0)
    #editor.save('labels')

    print 'scan gz files'
    datadir = './out/AMAP/roadlabel_poilabel/18'
    dirs = []
    files = []
    # 遍历目录
    for parent,dirnames,filenames in os.walk(datadir):
        for dirname in dirnames:
            dirs.append(os.path.join(parent, dirname))
        for filename in filenames:
            if (filename.lower().endswith('.gz') == False): continue
            files.append(os.path.join(parent, filename))

    if (os.path.exists('labels18.shp') == False):
        # 创建一个SHP文件
        writer = shapefile.Writer(shapefile.POINT)
        writer.field('label', 'C', 80)
        writer.field('angle', 'N', decimal=4)
        writer.field('icon', 'N', decimal=4)
        writer.field('size', 'N', decimal=4)
        writer.field('fontcolor', 'C', 10)
        writer.field('backcolor', 'C', 10)
        writer.field('icontype', decimal=4)
        writer.field('uid', 'C', 12)
        writer.field('code', 'C', 20)
        writer.save('labels18')
        print 'Create SHP finish.'

    #
    editor = shapefile.Editor('labels18')

    num = 0
    count = len(files)
    for fz in files:
        #
        num += 1
        print '[%04d/%d]: %s' % (num, count, fz)
        f = open(fz, 'rb')
        zdata = f.read()
        f.close()
        cdata = StringIO.StringIO(zdata)
        udata = gzip.GzipFile(fileobj=cdata).read()
        # 保存数据
        TileToSHP(udata, editor)
        

    # 保存
    editor.save('labels18')
    
            
