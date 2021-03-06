#!/usr/bin/python
# coding=utf-8
from StringIO import StringIO
from math import ceil, log

__author__ = "Aleksandr Shyshatsky"


class BitReader(object):
    def __init__(self, stream):
        # TODO: leave only one type here
        if isinstance(stream, str):
            self._stream = StringIO(stream)
        else:
            self._stream = stream

        self._bits_cache = []
        self._read_bits = 0

    @staticmethod
    def bits_required(length):
        if length < 1:
            return 0
        return int(ceil(log(length, 2)))

    @property
    def bytes_read(self):
        return int(ceil(self._read_bits / 8.0))

    def get_rest(self):
        return self._stream.read()

    def _iter_string_bits(self, string):
        for b in map(ord, string):
            for i in reversed(range(8)):
                yield (b >> i) & 1  # 0b00..[0|1]

    def _get_next_byte(self):
        next_byte = self._stream.read(1)
        if next_byte == '':
            raise Exception('I am empty %s' % self._read_bits)
        return next_byte

    def _get_next_bit(self):
        if not self._bits_cache:
            next_byte = self._get_next_byte()
            self._bits_cache = list(
                self._iter_string_bits(next_byte))

        self._read_bits += 1
        try:
            return self._bits_cache.pop(0)
        except IndexError:
            raise Exception('I am empty %s' % self._read_bits)

    def get(self, nbits):
        if nbits == 0:
            return 0

        value = 0
        while nbits > 0:
            bit = self._get_next_bit()
            value = (value << 1) | bit  # add bit to number
            nbits -= 1
        return value
