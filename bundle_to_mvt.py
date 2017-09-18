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
        self._fname = fname
        pass

    def GetTileMVT(self, position):
        # 获取单张瓦片mvt
        # position 偏移量
        pass

    def CreateNew(self, startrow, startcol):
        # 创建新的瓦片存储文件
        pass

    def InsertData(self, mvtdata):
        # 插入一块新瓦片到文件末尾
        pass

    def GetTilePosition(self, row, col):
        # 计算row行col列瓦片的偏移量
        pass

    def GetIndexPostion(self, row, col):
        # 计算row行col列在索引文件bundlx的偏移量
        pass

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
        
        bundlename = dirname + '/' + filename
        return bundlename

    def GetBundleRowCol(self, row, col):
        # 获取起始的行号和列号
        row = int(row / 128)
        row = row * 128
        col = int(col / 128)
        col = col * 128
        return row, col

    def GetTileXYZ(self, index):
        # 反推出瓦片XYZ
        fname = self._fname
        pass

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

    def ListTiles(self, startrow, startcol):
        # 列出瓦片包里有效的瓦片
        result = []
        fbundle = open(self._fname, 'rb')
        # 跳过头部64字节
        fbundle.seek(64)
        for col in range(startcol, startcol + 128):
            for row in range(startrow, startrow + 128):
                # 前5字节偏移量 后3个字节文件大小
                values = fbundle.read(8)
                offset = self.HexToInt5(values[0:5])    # 偏移量
                tsize = self.HexToInt3(values[5:8])     # 瓦片大小
                #
                if (tsize <= 0): continue
                tileinfo = {
                    'row': row,
                    'col': col,
                    'offset': offset,
                    'tsize': tsize
                    }
                result.append(tileinfo)
        fbundle.close()
        #
        return result

    def ReadTile(self, level, row, col):
        # 读取瓦片数据
        pass
    
    def WriteTile(self, level, row, col, data):
        # 写入瓦片数据
        pass



# =======================================================================

if __name__=='__main__':
    print '[==DoDo==]'
    print 'voter tiles.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 单元测试
    bundle = BundleClass('data/L14/R1b80C3300.bundle')

    # 根据瓦片等级/X/Y获得所在瓦片包名
    #print bundle.GetBundleName(14, 0x1b9b, 0x337b)

    # 获取文件名和目录名
    level, row, col = bundle.GetLevelRowCol()
    print level, row, col

    # 列出有效瓦片
    row, col = 7040, 13056
    tilelst = bundle.ListTiles(row, col)
    print len(tilelst)





    
