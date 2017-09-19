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


def GzipCompress(raw_data):
    # 压缩
    buf = StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf)
    try:
        f.write(raw_data)
    finally:
        f.close()
    return buf.getvalue()
  
def GzipUncompress(c_data):
    # 解压
    buf = StringIO(c_data)
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data

def CompressFile(fn_in, fn_out):
    # 压缩文件
    f_in = open(fn_in, 'rb')
    f_out = gzip.open(fn_out, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
  
def UncompressFile(fn_in, fn_out):
    # 解压文件
    f_in = gzip.open(fn_in, 'rb')
    f_out = open(fn_out, 'wb')
    file_content = f_in.read()
    f_out.write(file_content)
    f_out.close()
    f_in.close()

def ReadTile(fname, position):
    # 读取瓦片
    # fname: 文件名
    # position: 偏移量
    fbundle = open(fname, 'rb')
    fbundle.seek(position)
    value = fbundle.read(4)
    size = struct.unpack('i', value)[0]
    if (size == 0): tile = None
    else: tile = fbundle.read(size)
    fbundle.close()
    return tile

if __name__=='__main__':
    print '[==DoDo==]'
    print 'voter tiles.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    start = 0x20040
    for i in range(1, 100000):
        # 读取一张瓦片
        print hex(start)
        zdata = ReadTile('L14_R1b80C3300.bundle', start)
        if (zdata == None or len(zdata) == 0): break
        start = start + 4 + len(zdata)
        fsave = open('out/tile{0}.z'.format(i), 'wb')
        fsave.write(zdata)
        fsave.flush()
        fsave.close()

        # 解压一张瓦片
        #udata = zlib.decompress(zdata)
        cdata = StringIO.StringIO(zdata)
        udata = gzip.GzipFile(fileobj=cdata).read()
        fsave = open('out/tile{0}.u'.format(i), 'wb')    # 解压后的真实数据
        fsave.write(udata)
        fsave.flush()
        fsave.close()


    ''' 代码块1
    # 读取一张瓦片
    zdata = ReadTile('L14_R1b80C3300.bundle', 0x20040)
    fsave = open('tile1.z', 'wb')
    fsave.write(zdata)
    fsave.flush()
    fsave.close()

    # 解压一张瓦片
    #udata = zlib.decompress(zdata)
    cdata = StringIO.StringIO(zdata)
    udata = gzip.GzipFile(fileobj=cdata).read()
    fsave = open('tile1.u', 'wb')    # 解压后的真实数据
    fsave.write(udata)
    fsave.flush()
    fsave.close()

    # 压缩
    CompressFile('tile1.u', 'tile1.x')
    #print binascii.hexlify(out_data)
    '''


    print 'OK.'
