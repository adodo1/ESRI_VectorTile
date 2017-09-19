#!/usr/bin/env python
# encoding: utf-8

import os, sys, requests, struct, zlib, gzip, StringIO

# bundle瓦片定义
#
# 前64字节 =头部定义=
# 00-23: 未知
# 24-27: bundle文件大小
# 28-51: 未知
# 52-55: 瓦片个数 128*128个
# 56-63: 未知

# 64-131135:
#   每组8字节 总共 128 * 128 组
#   每组 0-4字节(5字节): 瓦片数据偏移量
#   每组 5-7字节(3字节): 文件大小

# 131136-:
#   真实瓦片数据
#   4字节瓦片大小
#   瓦片数据
#   4字节瓦片大小
#   瓦片数据
#   ...


# ESRI LODs
# level resolution          scale
# 00    78271.516963999995  295828763.79577750
# 01    39135.758481999947  147914381.89788851
# 02    19567.879241000050  73957190.948944494
# 03    9783.9396204999503  36978595.474472001
# 04    4891.9698102499797  18489297.737236001
# 05    2445.9849051249898  9244648.8686180003
# 06    1222.9924525624949  4622324.4343090001
# 07    611.49622628124496  2311162.2171545001
# 08    305.74811314069001  1155581.1085775001
# 09    152.87405657027901  577790.55428849999
# 10    76.437028285205500  288895.27714450000
# 11    38.218514142536598  144447.63857200000
# 12    19.109257071268299  72223.819285999998
# 13    9.5546285356341496  36111.909642999999
# 14    4.7773142678170748  18055.954821500000
# 15    2.3886571339746849  9027.9774109999998
# 16    1.1943285669873400  4513.9887054999999
# 17    0.59716428342752503 2256.9943524999999
# 18    0.29858214177990849 1128.4971765000000
# 19    0.14929107082380849 564.24858800000004


class GZipClass:
    def GzipCompress(self, raw_data):
        # 压缩
        buf = StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(raw_data)
        finally:
            f.close()
        return buf.getvalue()
      
    def GzipUncompress(self, c_data):
        # 解压
        buf = StringIO(c_data)
        f = gzip.GzipFile(mode = 'rb', fileobj = buf)
        try:
            r_data = f.read()
        finally:
            f.close()
        return r_data

    def CompressFile(self, fn_in, fn_out):
        # 压缩文件
        f_in = open(fn_in, 'rb')
        f_out = gzip.open(fn_out, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
      
    def UncompressFile(self, fn_in, fn_out):
        # 解压文件
        f_in = gzip.open(fn_in, 'rb')
        f_out = open(fn_out, 'wb')
        file_content = f_in.read()
        f_out.write(file_content)
        f_out.close()
        f_in.close()


class BundleClass:
    # 瓦片文件类
    def __init__(self, fname):
        # 初始化
        self._fname = fname         # bundle文件名
        self._tilesoffset = {}      # 偏移量字典 KEY:(row, col) VALUE:(offset, size)
        pass

    def GetTileMVT(self, offset, size):
        # 获取单张瓦片mvt 通过偏移量
        # offset 偏移量
        # size 文件大小
        if (size == 0): return None
        fbundle = open(self._fname, 'rb')
        fbundle.seek(offset)
        zdata = fbundle.read(size)
        fbundle.close()
        # 解压
        cdata = StringIO.StringIO(zdata)
        udata = gzip.GzipFile(fileobj=cdata).read()
        return udata

    def CreateNew(self, startrow, startcol):
        # 创建新的瓦片存储文件
        pass

    def InsertData(self, mvtdata):
        # 插入一块新瓦片到文件末尾
        pass

    def GetTileOffsetSize(self, row, col):
        # 计算row行col列瓦片数据位置和大小
        # row 总体行号
        # col 总体列号

        # 检查字典里有没有保存
        if (row, col) in self._tilesoffset.keys():
            offset, size = self._tilesoffset[(row, col)]
            return offset, size

        # 从文件中获取偏移量
        position = self.GetIndexPosition(row, col)
        fbundle = open(self._fname, 'rb')
        fbundle.seek(position)
        values = fbundle.read(8)
        fbundle.close()
        offset = self.HexToInt5(values[0:5])    # 偏移量
        size = self.HexToInt3(values[5:8])      # 瓦片大小
        
        # 保存在字典里
        self._tilesoffset[(row, col)] = (offset, size)
        return offset, size

    def GetIndexPosition(self, row, col):
        # 计算row行col列在bundle文件的索引偏移量
        # row 总体行号
        # col 总体列号
        row = row % 128
        col = col % 128
        # 跳过开始64字节 每组数据8字节
        base_pos = 64 + col * 8 * 128
        offset = row * 8
        position = base_pos + offset
        return position

    def HexToInt5(self, value):
        # 字节转整形
        # 例如: 0xFF00000000
        # 反序: 0x00000000FF
        # 再转成整数: 255

        #value = value + '000000'.decode('hex')
        #result = struct.unpack('q', value)[0]
        result = (ord(value[4]) & 0xFF) << 32 | \
                 (ord(value[3]) & 0xFF) << 24 | \
                 (ord(value[2]) & 0xFF) << 16 | \
                 (ord(value[1]) & 0xFF) << 8 | \
                 (ord(value[0]) & 0xFF)
        return int(result)

    def HexToInt3(self, value):
        # 字节转整形
        # 例如: 0xFF0000
        # 反序: 0x0000FF
        # 再转成整数: 255
        result = (ord(value[2]) & 0xFF) << 16 | \
                 (ord(value[1]) & 0xFF) << 8 | \
                 (ord(value[0]) & 0xFF)
        return int(result)

    def IntToHex(self, value):
        # 整形转5字节
        result = struct.pack('q', value)[0:5]
        return result

    def GetTileXYZ(self, index):
        # 反推出瓦片XYZ
        # index 索引值范围[0, 128*128)
        level, srow, scol = self.GetLevelRowCol()
        col = scol + int(index / 128)
        row = srow + index % 128
        return level, row, col

    def GetLevelRowCol(self):
        # 解析文件名 例如: L12/R0680C0c80.bundle
        # 得到整个bundle瓦片包的开始 等级/行号/列号
        fname = self._fname
        bundledir, bundlename = os.path.split(fname)
        bundledir = os.path.split(bundledir)[1]
        shotname, extension = os.path.splitext(bundlename)
        # 获取等级
        try:
            level = int(bundledir[1:])
        except ValueError as ex:
            level = -1
        # 获取行列
        try:
            row = int(shotname[1:5], 16)
            col = int(shotname[6:10], 16)
        except ValueError as ex:
            row = 0
            col = 0
        #
        return level, row, col

    def ListTiles(self, level=0, startrow=0, startcol=0):
        # 列出瓦片包里有效的瓦片
        # 从左上角相对瓦片(0,0)开始
        # level 等级
        # startrow 开始行
        # startcol 开始列
        result = []
        fbundle = open(self._fname, 'rb')
        # 跳过头部64字节
        fbundle.seek(64)
        for col in range(startcol, startcol + 128):
            for row in range(startrow, startrow + 128):
                # 前5字节偏移量 后3个字节文件大小
                values = fbundle.read(8)
                offset = self.HexToInt5(values[0:5])    # 偏移量
                size = self.HexToInt3(values[5:8])      # 瓦片大小
                #
                if (size <= 0): continue
                tileinfo = {
                    'level': level,
                    'row': row,
                    'col': col,
                    'offset': offset,
                    'size': size
                    }
                result.append(tileinfo)
        fbundle.close()
        #
        return result


class TileDataClass:
    # 瓦片数据处理类
    def __init__(self, tiledir):
        self._bundles = {}
        self._tiledir = tiledir

    def GetBundleName(self, level, row, col):
        # 通过等级 行号 列号获取集合名字
        # row 总体行号
        # col 总体列号
        # returns the name of the bundle that will hold the image
        # if it exists given the row and column of that image
        # round down to nearest 128
        row = int(row / 128)
        row = row * 128
        col = int(col / 128)
        col = col * 128
        row = '%04x' % row
        col = '%04x' % col
        filename = 'R{}C{}'.format(row, col)
        # 
        dirname = 'L%02d' % int(level)
        #
        bundlename = dirname + '/' + filename
        return bundlename

    def GetBundleRowCol(self, row, col):
        # 获取起始的行号和列号
        row = int(row / 128)
        row = row * 128
        col = int(col / 128)
        col = col * 128
        return row, col
        
    def ReadTile(self, level, row, col):
        # 读取瓦片数据
        # level 等级
        # row 总体行号
        # col 总体列号
        name = self.GetBundleName(level, row, col)
        bundlename = os.path.join(self._tiledir, name + '.bundle')
        if (os.path.exists(bundlename) == False ): return None

        if bundlename not in self._bundles.keys():
            self._bundles[bundlename] = BundleClass(bundlename)

        bundle = self._bundles[bundlename]
        # 计算瓦片数据偏移量和大小 读取瓦片数据
        offset, size = bundle.GetTileOffsetSize(row, col)
        mvtdata = bundle.GetTileMVT(offset, size)
        #
        return mvtdata

    def ListBundles(self):
        # 列出所有有效的瓦片包
        dirs = []
        files = []
        # 遍历目录
        for parent,dirnames,filenames in os.walk(self._tiledir):
            for dirname in dirnames:
                dirs.append(os.path.join(parent, dirname))
            for filename in filenames:
                files.append(os.path.join(parent, filename))
        #
        result = []
        for fname in files:
            shotname, extension = os.path.splitext(fname)
            if (extension.lower() == '.bundle'):
                result.append(fname)
        return result

    def ListTiles(self, bundlename):
        # 列出某个瓦片包里所有有效瓦片
        if (os.path.exists(bundlename) == False ): return None
        if bundlename not in self._bundles.keys():
            self._bundles[bundlename] = BundleClass(bundlename)
        bundle = self._bundles[bundlename]

        level, srow, scol = bundle.GetLevelRowCol()
        result = bundle.ListTiles(level, srow, scol)
        return result

    def SaveToDir(self, outdir, esri=False):
        # 保存碎瓦片到目录
        bundlelst = self.ListBundles()
        for bundlename in bundlelst:
            self.SaveOneToDir(bundlename, outdir)

    def SaveOneToDir(self, bundlename, outdir, esri=False):
        # 保存某一个bundle文件里的碎瓦片
        # bundlename 瓦片包文件
        # outdir 输出目录
        # esri 是否为Esri目录结构
        tilelst = tiledata.ListTiles(bundlename)
        for tile in tilelst:
            #
            level = tile['level']
            row = tile['row']
            col = tile['col']
            offset = tile['offset']
            size = tile['size']

            print '>> ', level, row, col
            #
            mvtdata = self.ReadTile(level, row, col)
            if (mvtdata == None or len(mvtdata) == 0): continue
            # 保存
            if (esri):
                savedir = os.path.join(outdir, 'L%02d/R%08x/' % (level, row))
                savename = 'C%08x.pbf' % col
                if (os.path.exists(savedir) == False):
                    os.makedirs(savedir)
            else:
                savedir = os.path.join(outdir, '%d/%d/' % (level, row))
                savename = '%d.pbf' % col
                if (os.path.exists(savedir) == False):
                    os.makedirs(savedir)
            savefile = open(savedir + savename, 'wb')
            savefile.write(mvtdata)
            savefile.flush()
            savefile.close()
    
    def WriteTile(self, level, row, col, data):
        # 写入瓦片数据
        pass


# =======================================================================

if __name__=='__main__':
    print '[==DoDo==]'
    print 'voter tiles.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    '''
    # 单元测试
    bundle = BundleClass('data/L14/R1b80C3300.bundle')
    tiledata = TileDataClass('data')

    # 根据瓦片等级/X/Y获得所在瓦片包名
    print tiledata.GetBundleName(14, 0x1b9b, 0x337b)

    # 获取文件名和目录名
    level, row, col = bundle.GetLevelRowCol()
    print level, row, col

    # 列出有效瓦片
    level = 14
    row, col = 7040, 13056
    tilelst = bundle.ListTiles(level, row, col)
    print len(tilelst)

    # 读取一块瓦片数据
    level = 14
    row, col = 7160, 13060
    mvtdata = tiledata.ReadTile(level, row, col)
    if mvtdata != None: print len(mvtdata)
    else: print 'Null Tile.'

    # 列出所有瓦片包
    bundlelst = tiledata.ListBundles()
    print len(bundlelst)

    # 列出某个瓦片包里有效的瓦片
    tilelst = tiledata.ListTiles(bundlelst[0])
    print bundlelst[0]
    print len(tilelst)
    print tilelst
    '''
    
    #
    tiledata = TileDataClass('data')
    tiledata.SaveToDir('out', False)


    print 'OK.'
    
