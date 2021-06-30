#usr/bin/python3
"""
Unit tests for the module codecs_lib.xor_scrambler

Covered classes:
    XOR_Coder
"""

__version__ = "1.0.0.0"
__date__ = "30-06-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import os
import sys
from typing import Type
import unittest

#+ modules to be tested

#+ my libraries

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
LIB_FOLDER = os.path.dirname(TEST_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from codecs_lib.xor_scrambler import XOR_Coder

#classes

#+ test cases

class Test_XOR_Coder(unittest.TestCase):
    """
    Test cases for the the codecs_lib.xor_scrambler.XOR_Coder class.
    
    Test ids TEST-T-400, TEST-T-401, TEST-T-402 and TEST-T-403.
    Covers the requirements REQ-FUN-401, REQ-FUN-410, REQ-FUN-420, REQ-AWM-400
    and REQ-AWM-401.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = XOR_Coder
        cls.SimpleTests = [
            (b'\x00', b'\xff'),
            (b'\x00\x01', b'\xff\xfe'),
            (b'\x00\x01\xaa', b'\xff\xfe\x55'),
            (b'\x00\x01\xaa\x55', b'\xff\xfe\x55\xaa'),
            (b'\x00\x01\xaa\x55', b'\xff\xfe\x55\xaa'),
            (b'\x00\x01\xaa\x55\xfe', b'\xff\xfe\x55\xaa\x01'),
            (b'\x00\x01\xaa\x55\xfe\xff', b'\xff\xfe\x55\xaa\x01\x00')
        ]
        cls.ComplexOriginal = 'anton\u2600антон'
        cls.ComplexEncoded = {
            'utf_8' : b''.join([b'\x9e\x91\x8b\x90\x91',
                                b'\x1d\x67\x7f',
                                b'\x2f\x4f\x2f\x42\x2e\x7d\x2f\x41\x2f\x42']),
            'utf_16_le' : b''.join([b'\x9e\xff\x91\xff\x8b\xff\x90\xff\x91\xff',
                                b'\xff\xd9',
                                b'\xcf\xfb\xc2\xfb\xbd\xfb\xc1\xfb\xc2\xfb']),
            'utf_32_le' : b''.join([b'\x9e\xff\xff\xff\x91\xff\xff\xff',
                                b'\x8b\xff\xff\xff\x90\xff\xff\xff',
                                b'\x91\xff\xff\xff',
                                b'\xff\xd9\xff\xff',
                                b'\xcf\xfb\xff\xff\xc2\xfb\xff\xff',
                                b'\xbd\xfb\xff\xff\xc1\xfb\xff\xff',
                                b'\xc2\xfb\xff\xff'])
        }
        cls.lstBadInput = [bytes, str, bytearray, 1, 1.2, [b'\x03'],
                            (b'\x03', 1), {'a' : 'b'}]
    
    def test_XOR_Coder_encode(self):
        """
        Tests the correctness of the implementation of the encoding.
        
        Test id TEST-T-400. Covers the requirements REQ-FUN-401 and REQ-FUN-410.
        
        Version 1.0.0.0
        """
        for bsOriginal, bsExpected in self.SimpleTests:
            #from bytestring
            bsTest = self.TestClass.encode(bsOriginal)
            self.assertEqual(bsTest, bsExpected)
            self.assertIsInstance(bsTest, bytes)
            #from bytearray
            bsTest = self.TestClass.encode(bytearray(bsOriginal))
            self.assertEqual(bsTest, bsExpected)
            self.assertIsInstance(bsTest, bytes)
        for strEncoding, bsExpected in self.ComplexEncoded.items():
            bsTest = self.TestClass.encode(self.ComplexOriginal,
                                                        Encoding = strEncoding)
            self.assertEqual(bsTest, bsExpected)
            self.assertIsInstance(bsTest, bytes)
        bsExpected = self.ComplexEncoded['utf_8']
        bsTest = self.TestClass.encode(self.ComplexOriginal)
        self.assertEqual(bsTest, bsExpected)
        self.assertIsInstance(bsTest, bytes)
        bsTest = self.TestClass.encode(self.ComplexOriginal, Encoding = None)
        self.assertEqual(bsTest, bsExpected)
        self.assertIsInstance(bsTest, bytes)
    
    def test_XOR_Coder_decode(self):
        """
        Tests the correctness of the implementation of the decoding.
        
        Test id TEST-T-401. Covers the requirements REQ-FUN-401 and REQ-FUN-420.
        
        Version 1.0.0.0
        """
        for bsOriginal, bsExpected in self.SimpleTests:
            #from bytestring
            bsTest = self.TestClass.decode(bsExpected)
            self.assertEqual(bsTest, bsOriginal)
            self.assertIsInstance(bsTest, bytes)
            #from bytearray
            bsTest = self.TestClass.decode(bytearray(bsExpected))
            self.assertEqual(bsTest, bsOriginal)
            self.assertIsInstance(bsTest, bytes)
        for strEncoding, bsExpected in self.ComplexEncoded.items():
            strTest = self.TestClass.decode(bsExpected, Encoding = strEncoding)
            self.assertEqual(strTest, self.ComplexOriginal)
            self.assertIsInstance(strTest, str)
    
    def test_XOR_Coder_TypeError(self):
        """
        Tests the handling of the improper input types.
        
        Test id TEST-T-402. Covers the requirements REQ-AWM-400.
        
        Version 1.0.0.0
        """
        for gInput in self.lstBadInput:
            with self.assertRaises(TypeError):
                self.TestClass.encode(gInput)
            with self.assertRaises(TypeError):
                self.TestClass.encode('test', Encoding = gInput)
            #no exception should be raised - second argument is ignored
            self.TestClass.encode(b'\x00', Encoding = gInput)
            self.TestClass.encode(bytearray(b'\x00'), Encoding = gInput)
            with self.assertRaises(TypeError):
                self.TestClass.decode(gInput)
            with self.assertRaises(TypeError):
                self.TestClass.decode(b'\x00', Encoding = gInput)
            with self.assertRaises(TypeError):
                self.TestClass.decode(bytearray(b'\x00'), Encoding = gInput)
        #special case - string input for decoding
        with self.assertRaises(TypeError):
            self.TestClass.decode('test')
    
    def test_XOR_Coder_ValueError(self):
        """
        Tests the handling of the improper input values - wrong codec.
        
        Test id TEST-T-403. Covers the requirements REQ-AWM-401.
        
        Version 1.0.0.0
        """
        #expected UnicodeError from codecs
        with self.assertRaises(ValueError):
            self.TestClass.encode(self.ComplexOriginal, Encoding = 'ascii')
        #unregistred codec
        with self.assertRaises(ValueError):
            self.TestClass.encode(self.ComplexOriginal, Encoding = 'ascii2')
        #expected UnicodeError from codecs
        with self.assertRaises(ValueError):
            self.TestClass.decode(self.ComplexEncoded['utf_8'],
                                                            Encoding = 'ascii')
        #unregistred codec
        with self.assertRaises(ValueError):
            self.TestClass.decode(self.ComplexEncoded['utf_8'],
                                                            Encoding = 'ascii2')

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_XOR_Coder)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1,])

if __name__ == "__main__":
    sys.stdout.write("Testing codecs_lib.xor_scrambler.XOR_Coder class...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)