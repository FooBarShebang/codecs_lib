#usr/bin/python3
"""
Unit tests for the module codecs_lib.vigenere

Covered classes:
    CircularList
"""

__version__ = "1.0.0.0"
__date__ = "07-07-2021"
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

from codecs_lib.vigenere import CircularList

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

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_CircularList)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1,])

if __name__ == "__main__":
    sys.stdout.write("Testing codecs_lib.vigenere module...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)