import os

class RaidDevice(object):
    def __init__(self, volumes, level, stripe_size, disk_size=0, offset=0, rotation='left', algorithm='asynchronous'):
        if level not in (0, 5):
            raise Exception('Raid level must be 0 or 5')
        self.level = level
        if self.level == 0:
            if len(volumes) < 2:
                raise Exception('Raid level 0 requires at least 2 volumes')
        elif self.level == 5:
            if len(volumes) < 3:
                raise Exception('Raid level 5 requires at least 3 volumes')
        if type(stripe_size) not in (int, long):
            raise Exception('Stripe size must be an integer')
        if type(offset) not in (int, long):
            raise Exception('Offset must be an integer')
        if type(disk_size) not in (int, long):
            raise Exception('Disk size must be an integer')
        if rotation not in ('left', 'right'):
            raise Exception('Rotation must be left or right')
        if algorithm not in ('asynchronous', 'synchronous'):
            raise Exception('Algorithm must be synchronous or asynchronous')
        self.volumes = [open(v, 'r') for v in volumes]
        self.volume_names = volumes
        self.stripe_size = stripe_size
        self.disk_size = disk_size
        self.offset = offset
        self.volume_count = len(self.volumes)
        self.rotation = rotation
        self.algorithm = algorithm
    def get_physical_stripe_number(self, logical_block):
        if self.level == 0:
            return logical_block / self.volume_count
        if self.level == 5:
            return logical_block / (self.volume_count - 1)
    def get_stripe_map(self, physical_stripe_number):
        if self.level == 0:
            start = physical_stripe_number * self.volume_count
            return range(start, start + self.volume_count)
        if self.level == 5:
            start = physical_stripe_number * (self.volume_count - 1)
            if self.rotation == 'left':
                parity_pos = (self.volume_count - 1) - physical_stripe_number % self.volume_count
            elif self.rotation == 'right':
                parity_pos = physical_stripe_number % self.volume_count
            map = []
            if self.algorithm == 'asynchronous':
                map.extend(range(start, start + parity_pos))
                map.append('P')
                map.extend(range(start + parity_pos, start + self.volume_count - 1))
            if self.algorithm == 'synchronous':
                stripe_start = start + self.volume_count - parity_pos - 1
                map.extend(range(stripe_start, stripe_start + parity_pos)) 
                map.append('P')
                map.extend(range(start, stripe_start))
            return map
    def get_block(self, block_number):
        physical_stripe = self.get_physical_stripe_number(block_number)
        stripe_map = self.get_stripe_map(physical_stripe)
        volume_index = stripe_map.index(block_number)
        self.volumes[volume_index].seek(physical_stripe * self.stripe_size + self.offset)
        return self.volumes[volume_index].read(self.stripe_size)
    def get_start_block(self, offset):
        return offset / self.stripe_size
    def get_block_offset(self, offset):
        return offset % self.stripe_size
    def read_blocks(self, length, offset=0):
        output = ''
        start_block = self.get_start_block(offset)
        block_offset = self.get_block_offset(offset)
        first_block = self.get_block(start_block)
        output += first_block[block_offset:]
        current_block = start_block + 1
        while len(output) < length:
            output += self.get_block(current_block)
            current_block += 1
        return output[:length]
    def read(self, length, offset=0):
        output = ''
        for block in self.read_blocks(length, offset):
            output += block
        return output
    def dump_blocks(self, length, offset=0, dump_block_size=65536):
        start = offset
        end = offset + length
        if length < dump_block_size:
            yield self.read(length, offset)
        else:
            for dump_pos in range(start, end, dump_block_size):
                yield self.read(dump_block_size, dump_pos)
    def size(self):
        if self.level == 0:
            volume_size = self.disk_size or os.path.getsize(self.volume_names[0])
            return (volume_size - self.offset) * self.volume_count
        if self.level == 5:
            volume_size = self.disk_size or os.path.getsize(self.volume_names[0])
            return (volume_size - self.offset) * (self.volume_count - 1)
    def close(self):
        [file.close() for file in self.volumes]
