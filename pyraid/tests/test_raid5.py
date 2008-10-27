#!/usr/bin/env python

import unittest
import pyraid

class ThreeDiskSS1Async(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        volume3 = 'fixtures/uvwxyz.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2, volume3), level=5, stripe_size=1, offset=0, rotation='left', algorithm='asynchronous')
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 12
    def test_read_all(self):
        assert self.raid.read(12) == '1a2vcw4d5yfz'
    def test_read_part_1(self):
        assert self.raid.read(5) == '1a2vc'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'w4d5y'
    def test_read_blocks(self):
        assert self.raid.get_block(0) == '1'
        assert self.raid.get_block(1) == 'a'
        assert self.raid.get_block(2) == '2'
        assert self.raid.get_block(3) == 'v'
    def test_stripe_map(self):
        assert self.raid.get_stripe_map(0) == [0, 1, 'P']
        assert self.raid.get_stripe_map(1) == [2, 'P', 3]
        assert self.raid.get_stripe_map(2) == ['P', 4, 5]
    def test_start_block(self):
        assert self.raid.get_start_block(0) == 0
        assert self.raid.get_start_block(1) == 1
        assert self.raid.get_start_block(2) == 2
class ThreeDiskSS1Sync(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        volume3 = 'fixtures/uvwxyz.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2, volume3), level=5, stripe_size=1, offset=0, rotation='left', algorithm='synchronous')
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 12
    def test_read_all(self):
        assert self.raid.read(12) == '1av2cw4dy5fz'
    def test_read_part_1(self):
        assert self.raid.read(5) == '1av2c'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'w4dy5'
    def test_read_blocks(self):
        assert self.raid.get_block(0) == '1'
        assert self.raid.get_block(1) == 'a'
        assert self.raid.get_block(2) == 'v'
        assert self.raid.get_block(3) == '2'
    def test_stripe_map(self):
        assert self.raid.get_stripe_map(0) == [0, 1, 'P']
        assert self.raid.get_stripe_map(1) == [3, 'P', 2]
        assert self.raid.get_stripe_map(2) == ['P', 4, 5]
    def test_start_block(self):
        assert self.raid.get_start_block(0) == 0
        assert self.raid.get_start_block(1) == 1
        assert self.raid.get_start_block(2) == 2
