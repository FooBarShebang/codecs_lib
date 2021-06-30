#usr/bin/python3
"""
Unit tests for the module codecs_lib.cobs

Covered classes:
    COBS_Coder
"""

__version__ = "1.0.0.0"
__date__ = "16-06-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import os
import sys
import unittest
import random

#+ modules to be tested

#+ my libraries

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
LIB_FOLDER = os.path.dirname(TEST_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from codecs_lib.cobs import COBS_Coder

#constants

TEST_BYTE_STRING = bytes(bytearray(i for i in range(1, 255)))
# b'\x01\x02...\xfd\xfe'

#classes

#+ test cases

class Test_COBS_Coder(unittest.TestCase):
    """
    Test cases for the the codecs_lib.cobs.COBS_Coder class.
    
    Test ids TEST-T-100, TEST-T-101, TEST-T-102, TEST-T-120 and TEST-T-121.
    Covers the requirements REQ-FUN-101, REQ-FUN-110, REQ-FUN-120, REQ-AWM-100
    and REQ-AWM-120.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = COBS_Coder
        cls.lstDecoded = [ b'\x00',
            b'\x00\x00', #all zeroes-package
            b'\x00\x00\x00\x00', #all zeroes-package
            b'\x11\x22\x00\x33', #zero in the middle of sequence
            b'\x11\x22\x33\x44', #short non-zero sequence
            b'\x11\x00\x00\x00', #many tailing zeroes
            TEST_BYTE_STRING, #exactly 254 non-zero characters package
            b''.join([b'\x00', TEST_BYTE_STRING]), # zero + 254 non-zero
            b''.join([TEST_BYTE_STRING, b'\xff']), #255 non-zero characters
            b''.join([TEST_BYTE_STRING[1:], b'\xff\x00']), #254 non-zero +1 zero
            b''.join([TEST_BYTE_STRING[2:], b'\xff\x00\x01']),
            #253 non-zero + 1 zero + one non-zero
            b''.join([TEST_BYTE_STRING, TEST_BYTE_STRING]), #2*254 non-zero
            b''.join([TEST_BYTE_STRING, b'\x00', TEST_BYTE_STRING]),
            #254 non-zero + zero + 254 non-zero
            b'\x2f\xa2\x00\x92\x73\x02',
            b'\x2f\xa2\x00\x92\x73\x26',
            ]
        cls.lstEncoded = [ b'\x01\x01',
            b'\x01\x01\x01',
            b'\x01\x01\x01\x01\x01',
            b'\x03\x11\x22\x02\x33',
            b'\x05\x11\x22\x33\x44',
            b'\x02\x11\x01\x01\x01',
            b''.join([b'\xff', TEST_BYTE_STRING]),
            b''.join([b'\x01\xff', TEST_BYTE_STRING]),
            b''.join([b'\xff', TEST_BYTE_STRING, b'\x02\xff']),
            b''.join([b'\xff', TEST_BYTE_STRING[1:], b'\xff\x01\x01']),
            b''.join([b'\xfe', TEST_BYTE_STRING[2:], b'\xff\x02\x01']),
            b''.join([b'\xff', TEST_BYTE_STRING, b'\xff', TEST_BYTE_STRING]),
            b''.join([b'\xff', TEST_BYTE_STRING, b'\x01\xff',
                                                            TEST_BYTE_STRING]),
            b'\x03\x2f\xa2\x04\x92\x73\x02',
            b'\x03\x2f\xa2\x04\x92\x73\x26'
            ]
        cls.lstBadInput = ['asd', bytes, str, bytearray, 1, 1.2, [b'\x03'],
                            (b'\x03', 1), {'a' : 'b'}]
    
    def test_COBS_Coder_decode(self):
        """
        Tests the correctness of the implementation of the decoding.
        
        Test id TEST-T-101. Covers the requirements REQ-FUN-101 and REQ-FUN-120.
        
        Version 1.0.0.0
        """
        for iIndex, bsSample in enumerate(self.lstEncoded):
            #from bytestring
            bsTest = self.TestClass.decode(bsSample)
            bsControl = self.lstDecoded[iIndex]
            self.assertEqual(bsTest, bsControl)
            self.assertIsInstance(bsTest, bytes)
            #from bytearray
            bsTest = self.TestClass.decode(bytearray(bsSample))
            self.assertEqual(bsTest, bsControl)
            self.assertIsInstance(bsTest, bytes)
    
    def test_COBS_Coder_encode(self):
        """
        Tests the correctness of the implementation of the encoding.
        
        Test id TEST-T-100. Covers the requirements REQ-FUN-101 and REQ-FUN-110.
        
        Version 1.0.0.0
        """
        for iIndex, bsSample in enumerate(self.lstDecoded):
            #from bytestring
            bsTest = self.TestClass.encode(bsSample)
            bsControl = self.lstEncoded[iIndex]
            self.assertEqual(bsTest, bsControl)
            self.assertIsInstance(bsTest, bytes)
            #from bytearray
            bsTest = self.TestClass.encode(bytearray(bsSample))
            self.assertEqual(bsTest, bsControl)
            self.assertIsInstance(bsTest, bytes)
    
    def test_COBS_Coder_decode_Strip(self):
        """
        Tests the correctness of the implementation of the decoding,
        specifically - removing of the leading and tailing zero characters.
        
        Test id TEST-T-120. Covers the requirements REQ-FUN-120.
        
        Version 1.0.0.0
        """
        for iIndex, bsSample in enumerate(self.lstEncoded):
            bsControl = self.lstDecoded[iIndex]
            for _ in range(10):
                iNLeading = random.randint(1, 10)
                iNTailing = random.randint(1, 10)
                bsLeading = b''.join([b'\x00' for _ in range(iNLeading)])
                bsTailing = b''.join([b'\x00' for _ in range(iNTailing)])
                bsInput = b''.join([bsLeading, bsSample, bsTailing])
                #from bytestring
                bsTest = self.TestClass.decode(bsInput)
                self.assertEqual(bsTest, bsControl)
                self.assertIsInstance(bsTest, bytes)
                #from bytearray
                bsTest = self.TestClass.decode(bytearray(bsInput))
                self.assertEqual(bsTest, bsControl)
                self.assertIsInstance(bsTest, bytes)
    
    def test_COBS_Coder_decode_Raises_ValueError(self):
        """
        Tests the decoder raises ValueError if there is at least one zero
        character ('\x00') in the input string, which is not in either leading
        or tailing position.
        
        Test id TEST-T-121. Covers the requirements REQ-AWM-120.
        
        Version 1.0.0.0
        """
        for iIndex, bsSample in enumerate(self.lstEncoded):
            bsControl = self.lstDecoded[iIndex]
            for _ in range(10):
                iNPosition = random.randint(1, len(bsSample) - 1)
                bsInput = b''.join([bsSample[:iNPosition], b'\x00',
                                                        bsSample[iNPosition:]])
                #from bytestring
                with self.assertRaises(ValueError):
                    bsTest = self.TestClass.decode(bsInput)
                #from bytearray
                baInput = bytearray(bsInput)
                with self.assertRaises(ValueError):
                    bsTest = self.TestClass.decode(baInput)
    
    def test_COBS_Coder_decode_Raises_TypeError(self):
        """
        Tests the decoder raises TypeError if the input is anything but an
        instance of bytearray or bytestring.
        
        Test id TEST-T-102. Covers the requirements REQ-AWM-100.
        
        Version 1.0.0.0
        """
        for gInput in self.lstBadInput:
            with self.assertRaises(TypeError):
                self.TestClass.decode(gInput)
    
    def test_COBS_Coder_encode_Raises_TypeError(self):
        """
        Tests the encoder raises TypeError if the input is anything but an
        instance of bytearray or bytestring.
        
        Test id TEST-T-102. Covers the requirements REQ-AWM-100.
        
        Version 1.0.0.0
        """
        for gInput in self.lstBadInput:
            with self.assertRaises(TypeError):
                self.TestClass.encode(gInput)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_COBS_Coder)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1,])

if __name__ == "__main__":
    sys.stdout.write("Testing codecs_lib.cobs.COBS_Coder class...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)