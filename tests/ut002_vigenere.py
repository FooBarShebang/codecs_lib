#usr/bin/python3
"""
Unit tests for the module codecs_lib.vigenere

Covered classes:
    CircularList
    VigenereCodec
"""

__version__ = "1.0.1.0"
__date__ = "27-07-2021"
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

from codecs_lib.vigenere import CircularList, VigenereCoder

#classes

#+ test cases

class Test_CircularList(unittest.TestCase):
    """
    Test cases for the the codecs_lib.vigener.CircularList class.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = CircularList
        cls.EmptySequences = [
            list(), tuple(), '', b'', bytearray(b'')
        ]
        cls.BadCases = [
            1, 2.0, True, int, float, bool, str, bytes, bytearray, list, tuple
        ]
        cls.TestCases = [
            'a',
            b'\x00',
            bytearray(b'\x00'),
            [1],
            ('a', ),
            'ab',
            b'\x00',
            bytearray(b'\x00a'),
            [1, 'b'],
            ('a', 2.0),
            'abc',
            b'\x00\x01\xff',
            bytearray(b'\x00ab'),
            [1, 2.0, 'a'],
            ('a', 2, 3.0),
            b'\x00abcdefghij',
            bytearray(b'\x00abd\xff'),
            [1, 'bc', b'ab'],
            ('a', 2.0, 1, 5),
            'anton\u2600антон'
        ]
    
    def test_init_ValueError(self):
        """
        Initialization should raise sub-class of ValueError if an empty
        sequence is passed.

        Version 1.0.0.0
        """
        for seqItem in self.EmptySequences:
            with self.assertRaises(ValueError):
                self.TestClass(seqItem)
    
    def test_init_TypeError(self):
        """
        Initialization should raise sub-class of TypeError if not a sequence is
        passed.

        Version 1.0.0.0
        """
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestClass(gItem)
    
    def test_setContent_ValueError(self):
        """
        setContent() method should raise sub-class of ValueError if an empty
        sequence is passed.

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for seqItem in self.EmptySequences:
            with self.assertRaises(ValueError):
                objTest.setContent(seqItem)
        del objTest
    
    def test_setContent_TypeError(self):
        """
        setContent() method should raise sub-class of TypeError if not a
        sequence is passed.

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                objTest.setContent(gItem)
        del objTest
    
    def test_getElement_Exception(self):
        """
        getElement() method should raise an exception when called with the
        content not being set.

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        with self.assertRaises(Exception):
            objTest.getElement()
        del objTest
    
    def test_getElement(self):
        """
        Checks that the getElement() method returns the proper elements of the
        stored sequence with each call. Also checks the proper implementation
        of the method setContent(), and instantiation with and without sequence
        argument.

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for seqItem in self.TestCases:
            iLength = len(seqItem)
            objTest.setContent(seqItem)
            for iCounter in range(100):
                iIndex = iCounter % iLength
                gTest = objTest.getElement()
                self.assertEqual(gTest, seqItem[iIndex])
        del objTest
        seqItem = self.TestCases[-1]
        objTest = self.TestClass(seqItem)
        iLength = len(seqItem)
        for iCounter in range(100):
            iIndex = iCounter % iLength
            gTest = objTest.getElement()
            self.assertEqual(gTest, seqItem[iIndex])
        del objTest
    
    def test_resetCounter(self):
        """
        Checks that the resetCounter() method properly sets the internal
        indexing to the first element of the stored sequence
        """
        objTest = self.TestClass()
        for seqItem in self.TestCases:
            objTest.setContent(seqItem)
            for _ in range(13):
                objTest.getElement()
            objTest.resetCounter()
            gTest = objTest.getElement()
            self.assertEqual(gTest, seqItem[0])
        del objTest

class Test_VigenereCoder(unittest.TestCase):
    """
    Test cases for the the codecs_lib.vigener.VigenereCoder class.

    Test ids TEST-T-200, TEST-T-201, TEST-T-202, TEST-T-203, TEST-T-204,
    TEST-T-210, TEST-T-220 and TEST-T-230.
    Covers the requirements REQ-FUN-202, REQ-FUN-203, REQ-FUN-210,
    REQ-FUN-220, REQ-FUN-230, REQ-AWM-200, REQ-AWM-201, REQ-AWM-202,
    REQ-AWM-203, REQ-AWM-210, REQ-AWM-220 and REQ-AWM-230.
    
    Version 1.1.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = VigenereCoder
        cls.BadTypes = [1, 2.0, True, ('a', ), ['a'], {"a" : 'a'}, str, int,
                        float, bool, list, tuple, bytes, bytearray]
        cls.NotString = list(cls.BadTypes)
        cls.NotString.extend([b'a', bytearray(b'a')])
        cls.NotBytes = list(cls.BadTypes)
        cls.NotBytes.append('a')
    
    def test_ContinuousFeed(self):
        """
        Test the implementation of the Vigenere codec specifically for the
        continuous data feed.

        Test id: TEST-T-200.
        Covers requirements: REQ-FUN-202, REQ-FUN-210 and REQ-FUN-220

        Version 2.0.0.0
        """
        #closure helper check function
        def InnerCheck(objTest: VigenereCoder, objC_List: CircularList,
                        InData: bytearray) -> None:
            #let the indexes shift first
            objTest.encode(InData.decode('utf_8'))
            for _ in range(len(InData)):
                objC_List.getElement()
            baTemp = bytearray()
            for InByte in InData:
                Code = objC_List.getElement()
                OutByte = objTest.encode(chr(InByte))
                self.assertIsInstance(OutByte, bytes)
                self.assertEqual(ord(OutByte), (InByte + Code) % 256)
                baTemp.append(ord(OutByte))
            #now for decoding
            #+ reset both indexes
            objTest.resetIndex()
            objC_List.resetCounter()
            #+let the indexes shift again by the same number of position
            objTest.encode(InData.decode('utf_8'))
            for _ in range(len(InData)):
                objC_List.getElement()
            for OutByte in baTemp:
                Decoded = objTest.decode(bytearray([OutByte]))
                self.assertIsInstance(Decoded, str)
                NewByte = ord(Decoded)
                Code1 = objC_List.getElement()
                self.assertEqual(NewByte, (OutByte - Code1) % 256)
        #test main body
        Password = bytearray(random.randint(0, 255)
                                        for _ in range(random.randint(5, 15)))
        objTest = self.TestClass(Password)
        objC_List = CircularList(Password)
        InData = bytearray(random.randint(0, 127)
                                    for _ in range(random.randint(50, 150)))
        InnerCheck(objTest, objC_List, InData)
        InData = bytearray(random.randint(0, 127)
                                    for _ in range(random.randint(50, 150)))
        objTest.resetIndex()
        objC_List.resetCounter()
        InnerCheck(objTest, objC_List, InData)
        InData = bytearray(random.randint(0, 127)
                                    for _ in range(random.randint(50, 150)))
        Password = bytearray(random.randint(0, 255)
                                        for _ in range(random.randint(5, 15)))
        objTest.setPassword(Password)
        objC_List.setContent(Password)
        InnerCheck(objTest, objC_List, InData)
        del objTest
        del objC_List

    def test_EncodingDecoding(self):
        """
        Test the implementation of the Vigenere codec concerning different
        allowed input data types.

        Test id: TEST-T-201.
        Covers requirements: REQ-FUN-210, REQ-FUN-220 and REQ-FUN-230

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        Password = 'an\u2600атн'
        Passwords = [Password, Password.encode('utf_8'),
                                                bytearray(Password, 'utf_8')]
        InData = 'anton\u2600антон'
        for PassPhrase in Passwords:
            objTest.setPassword(PassPhrase)
            for Codec in [None, 'utf_8', 'utf_16', 'utf_16_be', 'utf_16_le',
                                            'utf_32', 'utf_32_be', 'utf_32_le']:
                if not (Codec is None):
                    OutData = objTest.encode(InData, Codec = Codec)
                else:
                    OutData = objTest.encode(InData)
                self.assertIsInstance(OutData, bytes)
                objTest.resetIndex()
                for Temp in [OutData, bytearray(OutData)]:
                    if not (Codec is None):
                        NewData = objTest.decode(Temp, Codec = Codec)
                    else:
                        NewData = objTest.decode(Temp)
                    self.assertIsInstance(NewData, str)
                    self.assertEqual(NewData, InData)
                    objTest.resetIndex()
        del objTest
    
    def test_ValueError(self):
        """
        Tests that ValueError sub-class is raised if the Unicode codec is not
        registered or incompatible with the actual data.

        Test id: TEST-T-202.
        Covers requirement: REQ-AWM-200

        Version 1.0.0.0
        """
        objTest = self.TestClass(b'\x00')
        InData = 'anton\u2600антон'
        for Codec in ['ascii', 'cp1251', 'whatever']:
            with self.assertRaises(ValueError):
                objTest.encode(InData, Codec = Codec)
        OutData = objTest.encode(InData)
        for Codec in ['ascii', 'cp1251', 'utf_32', 'whatever']:
            with self.assertRaises(ValueError):
                objTest.decode(OutData, Codec = Codec)
        del objTest
    
    def test_TypeError(self):
        """
        Tests that TypeError sub-class is raised if the requested Unicode codec
        is not a string.

        Test id: TEST-T-203.
        Covers requirement: REQ-AWM-201

        Version 1.0.0.0
        """
        objTest = self.TestClass(b'\x00')
        InData = 'anton'
        OutData = objTest.encode(InData)
        for Codec in self.NotString:
            with self.assertRaises(TypeError):
                objTest.encode(InData, Codec = Codec)
            with self.assertRaises(TypeError):
                objTest.decode(OutData, Codec = Codec)
        del objTest
    
    def test_NoPassword(self):
        """
        Tests that an exception is raised if the password is not set before
        attempting to encode or decode.

        Test id: TEST-T-204.
        Covers requirement: REQ-AWM-202

        Version 2.0.0.0
        """
        objTest = self.TestClass()
        InData = 'anton'
        with self.assertRaises(Exception):
            objTest.encode(InData)
        with self.assertRaises(Exception):
            objTest.decode(bytes(InData, 'utf_8'))
        del objTest
    
    def test_Encode_TypeError(self):
        """
        Tests that TypeError sub-class is raised if the data argument passed
        into the encode method is not a string.

        Test id: TEST-T-210.
        Covers requirement: REQ-AWM-210.

        Version 1.0.0.0
        """
        objTest = self.TestClass(b'\x00')
        for Data in self.NotString:
            with self.assertRaises(TypeError):
                objTest.encode(Data)
        del objTest
    
    def test_Decode_TypeError(self):
        """
        Tests that TypeError sub-class is raised if the data argument passed
        into the decode method is neither a bytestring nor a bytes array.

        Test id: TEST-T-220.
        Covers requirement: REQ-AWM-220.

        Version 1.0.0.0
        """
        objTest = self.TestClass(b'\x00')
        for Data in self.NotBytes:
            with self.assertRaises(TypeError):
                objTest.decode(Data)
        del objTest
    
    def test_Password_TypeError(self):
        """
        Tests that TypeError sub-class is raised if the password passed into the
        'set passphrase' method is neither a bytestring nor a bytes array, nor a
        string.

        Test id: TEST-T-230.
        Covers requirement: REQ-AWM-230.

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for Password in self.BadTypes:
            with self.assertRaises(TypeError):
                objTest.setPassword(Password)
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_CircularList)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_VigenereCoder)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Testing codecs_lib.vigenere module...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)