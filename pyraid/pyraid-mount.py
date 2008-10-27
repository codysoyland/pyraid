#!/usr/bin/env python
import pyraid
import os, stat, errno
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)
raid_path = '/raid_device'

class BlankStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class RaidFS(Fuse):
    def __init__(self, raid_options, raid_volumes, *args, **kwargs):
        Fuse.__init__(self, *args, **kwargs)
        self.raid_dev = pyraid.RaidDevice(volumes=raid_volumes, level=int(raid_options.level), stripe_size=int(raid_options.stripe_size), offset=int(raid_options.offset))
        #self.size = self.raid_dev.size()
    def getattr(self, path):
        st = BlankStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path == raid_path:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = self.raid_dev.size()
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        for r in  '.', '..', raid_path[1:]:
            yield fuse.Direntry(r)

    def open(self, path, flags):
        if path != raid_path:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        if path != raid_path:
            return -errno.ENOENT
        slen = self.raid_dev.size()
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = self.raid_dev.read(size, offset)
        else:
            buf = ''
        return buf

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_usage('python pyraid-mount.py [options] volume1, volume2, [volume3,...]')
    parser.add_option('-l', '--level', dest='level', help='RAID level to use (0 or 5)', metavar='LEVEL', default=0)
    parser.add_option('-s', '--stripe-size', dest='stripe_size', help='Stripe size in bytes', metavar='BYTES', default=64*1024)
    parser.add_option('-o', '--offset', dest='offset', help='Physical offset of first stripe', metavar='BYTES', default=0)
    parser.add_option('-m', '--mount-point', dest='mount_point', help='Path to mount raw device', metavar='PATH', default='.')
    parser.add_option('-r', '--rotation', dest='rotation', help='Parity rotation direction for RAID-5 (left or right)', metavar='DIRECTION', default='left')
    parser.add_option('-a', '--algorithm', dest='algorithm', help='RAID-5 algorithm to use (synchronous or asynchronous)', default='synchronous')
    options, args = parser.parse_args() 

    import sys
    sys.argv = [sys.argv[0], options.mount_point, '-d'] # hack to set command line arguments to those that python-fuse will correctly parse

    usage="""
Usersrpace hello example

""" + Fuse.fusage
    server = RaidFS(options, args, version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
