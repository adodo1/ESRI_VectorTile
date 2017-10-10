#!/usr/bin/env python
# encoding: utf-8

import os, sys, requests, struct, zlib, gzip, StringIO

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

# =======================================================================

def UncompressPbf(fname):
    # 解压PBF文件
    f = open(fname, 'rb')
    zdata = f.read()
    f.close()
    #
    if (zdata[0] == 0x1F and zdata[1] ==0x8B):
        # 解压
        cdata = StringIO.StringIO(zdata)
        udata = gzip.GzipFile(fileobj=cdata).read()
        f = open(fname, 'wb')
        f.write(udata)
        f.close()
    

if __name__=='__main__':
    print '[==DoDo==]'
    print 'uncompress pbf.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    # 作用是解压所有压缩的pbf文件

    inpath = './'

    print 'scan files'
    dirs = []
    files = []
    # 遍历目录
    for parent,dirnames,filenames in os.walk(inpath):
        for dirname in dirnames:
            dirs.append(os.path.join(parent, dirname))
        for filename in filenames:
            fname, exname = os.path.splitext(filename)
            if (exname.lower()  != '.pbf'): continue
            files.append(os.path.join(parent, filename))
    
    print 'file count: %s' % len(files)

    count = len(files)
    num = 0
    for fname in files:
        num += 1
        print '[%d/%d] %s' %(num, count, fname)
        UncompressPbf(fname)

    print 'OK.'
    
