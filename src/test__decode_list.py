from unittest import TestCase

import readConfig1

__author__ = '0400428'


class Test_decode_list(TestCase):
    def test__decode_list_None(self):
        self.assertRaises(AttributeError, readConfig1._decode_dict, None)
    def test__decode_list_1(self):
        self.assertRaises(AttributeError, readConfig1._decode_dict, [1, 2, 3])

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=30).run(suite)

