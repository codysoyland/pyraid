#!/usr/bin/env python
import pyraid
import sys

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_usage('python pyraid-dump.py [options] volume1 volume2 [volume3...]')
    parser.add_option('-l', '--level', dest='level', help='RAID level to use (0 or 5)', metavar='LEVEL', default=0)
    parser.add_option('-s', '--stripe-size', dest='stripe_size', help='Stripe size in bytes', metavar='BYTES', default=64*1024)
    parser.add_option('-b', '--dump-block-size', dest='dump_block_size', help='Dump block size in bytes', metavar='BYTES', default=64*1024)
    parser.add_option('-d', '--disk-size', dest='disk_size', help='Disk size in bytes (optional override)', metavar='BYTES', default=0)
    parser.add_option('-o', '--offset', dest='offset', help='Physical offset of first stripe', metavar='BYTES', default=0)
    parser.add_option('-g', '--logical-offset', dest='logical_offset', help='Logical offset to begin dumping at', metavar='BYTES', default=0)
    parser.add_option('-r', '--rotation', dest='rotation', help='Parity rotation direction for RAID-5 (left or right)', metavar='DIRECTION', default='left')
    parser.add_option('-a', '--algorithm', dest='algorithm', help='RAID-5 algorithm to use (synchronous or asynchronous)', default='synchronous')
    raid_options, volumes = parser.parse_args() 

    raid_device = pyraid.RaidDevice(
        volumes = volumes,
        level = int(raid_options.level),
        stripe_size = int(raid_options.stripe_size),
        disk_size = int(raid_options.disk_size),
        offset = int(raid_options.offset),
        rotation = raid_options.rotation,
        algorithm = raid_options.algorithm,
    )
    
    dump_block_size = int(raid_options.dump_block_size),
    logical_offset = int(raid_options.logical_offset)
    for block in raid_device.dump_blocks(length=raid_device.size() - logical_offset, offset=logical_offset):
        sys.stdout.write(block)
    
if __name__ == '__main__':
    main()