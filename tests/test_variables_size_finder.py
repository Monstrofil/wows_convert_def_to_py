import unittest
from ddt import ddt, data, unpack

from def_generator.entities.helper import VariablesLengthHelper


@ddt
class MyTestCase(unittest.TestCase):
    def setUp(self):
        alias_map = {

        }
        self._tool = VariablesLengthHelper(alias_map)

    @data(
        # primitive types
        [['FLOAT'], 32],
        [['FLOAT32'], 32],
        [['FLOAT64'], 64],
        [['INT8'], 8],
        [['INT16'], 16],
        [['INT32'], 32],
        [['INT64'], 64],
        [['UINT8'], 8],
        [['UINT16'], 16],
        [['UINT32'], 32],
        [['UINT64'], 64],
        [['VECTOR2'], 2 * 32],
        [['VECTOR3'], 3 * 32],
        [['VECTOR4'], 4 * 32],

        # multiple primitives
        [['VECTOR4', 'INT8'], 4 * 32 + 8],
        [['UINT64', 'INT8'], 64 + 8],
        [['FLOAT', 'FLOAT'], 64],

        # fixed array
        [[['ARRAY', 'INT8', 2]], 2 * 8],
        [[['ARRAY', 'VECTOR4', 5]], 5 * 4 * 32],

        # nested fixed arrays
        [[['ARRAY', ['ARRAY', 'INT8', 3], 5]], 3 * 5 * 8],

        # dicts
        [[['FIXED_DICT', (('k1', 'INT8'),
                          ('k2', 'INT8'),
                          ('k3', 'INT64')), False]], 8 + 8 + 64],

        # variable length types
        ['STRING', 10**10],
        ['BLOB', 10**10],
        [['ARRAY', 'INT64'], 10**10],

        # nullable dict
        [[['FIXED_DICT', [('k1', 'INT8')], True]], 10**10],
    )
    @unpack
    def test_check_arguments_size(self, arguments, size):
        self.assertEqual(size, self._tool.get_variables_size(arguments))


if __name__ == '__main__':
    unittest.main()
