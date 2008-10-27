#!/usr/bin/env python

import unittest
import pyraid

class TwoDiskSS1(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/12345.txt'
        volume2 = 'fixtures/abcde.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2), level=0, stripe_size=1, offset=0)
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 10
    def test_read_all(self):
        assert self.raid.read(10) == '1a2b3c4d5e'
    def test_read_part_1(self):
        assert self.raid.read(5) == '1a2b3'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'c4d5e'
    def test_read_blocks(self):
        assert self.raid.get_block(0) == '1'
        assert self.raid.get_block(1) == 'a'
        assert self.raid.get_block(2) == '2'
        assert self.raid.get_block(3) == 'b'
    def test_stripe_map(self):
        assert self.raid.get_stripe_map(0) == [0, 1]
        assert self.raid.get_stripe_map(1) == [2, 3]
        assert self.raid.get_stripe_map(2) == [4, 5]
    def test_start_block(self):
        assert self.raid.get_start_block(0) == 0
        assert self.raid.get_start_block(1) == 1
        assert self.raid.get_start_block(2) == 2
class TwoDiskSS2(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2), level=0, stripe_size=2, offset=0)
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 12
    def test_read_all(self):
        assert self.raid.read(12) == '12ab34cd56ef'
    def test_read_part_1(self):
        assert self.raid.read(5) == '12ab3'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == '4cd56'
    def test_start_block(self):
        assert self.raid.get_start_block(0) == 0
        assert self.raid.get_start_block(1) == 0
        assert self.raid.get_start_block(2) == 1
class ThreeDiskSS2(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        volume3 = 'fixtures/uvwxyz.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2, volume3), level=0, stripe_size=2, offset=0)
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 18
    def test_read_all(self):
        assert self.raid.read(12) == '12abuv34cdwx'
    def test_read_part_1(self):
        assert self.raid.read(5) == '12abu'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'v34cd'
class ThreeDiskSS2Offset2(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        volume3 = 'fixtures/uvwxyz.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2, volume3), level=0, stripe_size=2, offset=2)
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 12
    def test_read_all(self):
        assert self.raid.read(12) == '34cdwx56efyz'
    def test_read_part_1(self):
        assert self.raid.read(5) == '34cdw'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'x56ef'
class ThreeDiskSS3(unittest.TestCase):
    def setUp(self):
        volume1 = 'fixtures/123456.txt'
        volume2 = 'fixtures/abcdef.txt'
        volume3 = 'fixtures/uvwxyz.txt'
        self.raid = pyraid.RaidDevice(volumes=(volume1, volume2, volume3), level=0, stripe_size=3, offset=0)
    def tearDown(self):
        self.raid.close()
    def test_size(self):
        assert self.raid.size() == 18
    def test_read_all(self):
        assert self.raid.read(12) == '123abcuvw456'
    def test_read_part_1(self):
        assert self.raid.read(5) == '123ab'
    def test_read_part_2(self):
        assert self.raid.read(5, 5) == 'cuvw4'
