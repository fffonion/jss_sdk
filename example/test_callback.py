from __future__ import print_function
from jss.connection import JssClient
import os
import time
import re
import sys
import urllib
import binascii
from hashlib import md5
reload(sys)
sys.setdefaultencoding('utf-8')
if len(sys.argv) < 2:
    raw_input('test_callback.py file')
    sys.exit(0)

jss = JssClient('ACCESS_KEY', 'SECRET_KEY',
                        'storage.jcloud.com')
buc_name = 'resource'
part_size = 5*1024*1024
def get_size_h(s):
    s = s/1024.0 #kb
    if s >=1024*900:
        return '%.2fG' % (s/1024/1024)
    if s >=900:
        return '%.2fM' % (s/1024)
    return '%.2fK' % s

def progress(idx, total, psize):
    print('\b' * 80 + ' '*70 + '\b'*80, end = '')
    print(' [%s] %s' % ('#' * (60 * (idx+1) / total) + ' ' * (60 - 60 * (idx+1) / total), get_size_h(min(os.stat(filep).st_size, psize * (idx+1)))), end = '')

filep = sys.argv[1]

if len(sys.argv) > 2:
    buc_name = sys.argv[2]
    
print('Use bucket:%s' % buc_name)


print('FILE:%s\nFile size is %s, part size is %s' % (filep, get_size_h(os.stat(filep).st_size), get_size_h(part_size)))
fn = os.path.basename(filep).decode('gbk').encode('utf-8')
o=jss.bucket(buc_name).object(fn)
a=time.time()
o.multi_upload(local_file_path = filep, part_size = part_size, callback = progress)
print('\nUploaded in %.2fs\n%s' % (time.time() - a, '-' * 70))