import unittest
from StringIO import StringIO

from def_generator.bit_reader import BitReader


class TestBigReader(unittest.TestCase):

    def test_read_bits_normally_all_array(self):
        s = StringIO('\x01')  # 0000 0001
        bit_reader = BitReader(s)

        self.assertEqual(0, bit_reader.get(1))
        self.assertEqual(1, bit_reader.get(7))

        self.assertEqual('', bit_reader.get_rest())

    def test_read_bits_normally_only_first_byte(self):
        s = StringIO('\xF0\x02')  # 1111 0000 0000 0010
        bit_reader = BitReader(s)

        self.assertEqual(1, bit_reader.get(1))
        self.assertEqual(3, bit_reader.get(2))
        self.assertEqual(2, bit_reader.get(2))

        self.assertEqual('\x02', bit_reader.get_rest())

    def test_read_bits_normally_two_bytes(self):
        s = StringIO('\xF0\x02')  # 1111 0000 0000 0010
        bit_reader = BitReader(s)

        self.assertEqual(1, bit_reader.get(1))
        self.assertEqual(3, bit_reader.get(2))
        self.assertEqual(2, bit_reader.get(2))
        self.assertEqual(0, bit_reader.get(8))
        self.assertEqual(2, bit_reader.get(3))

        self.assertEqual('', bit_reader.get_rest())


if __name__ == '__main__':
    unittest.main()
