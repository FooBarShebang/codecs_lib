#usr/bin/python3
"""
Unit tests for the module codecs_lib.wichmann_hill

Covered classes:
    WH_Generator
    WH_Coder
"""

__version__ = "1.0.0.0"
__date__ = "30-07-2021"
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

from codecs_lib.wichmann_hill import WH_Generator, WH_Coder

#classes

#+ test cases

class Test_WH_Generator(unittest.TestCase):
    """
    Test cases for the the codecs_lib.wichmann_hill.WH_Generator class.
    
    Test ids: TEST-T-310, TEST-T-311, TEST-T-312
    Covered requirements: REQ-FUN-310, REQ-AWM-300, REQ-AWM-301

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = WH_Generator
        cls.BadSeeds = [1.0, int, float, str, bytes, bytearray, '1', b'1', list,
                        tuple, dict, [1], (1, 1), [1, int], {1 : 1}]
        cls.TestSets = [
            [[1, 1, 1],
                [0.01693091, 0.89525391, 0.11149102, 0.93952680, 0.12822986,
                 0.17800399, 0.29982708, 0.34971841, 0.05928746, 0.82197931,
                 0.88139716, 0.16007288, 0.64780522, 0.48791600, 0.31410325]
            ],
            [[1, 2, 3],
                [0.03381877, 0.77754189, 0.05273525, 0.74462407, 0.49036219,
                 0.98285437, 0.80915099, 0.71338138, 0.80102091, 0.98958603,
                 0.91685632, 0.46664672, 0.67019946, 0.92749661, 0.84314959]
            ],
            [[1, 150503156, 10],
                [0.08230170, 0.03811720, 0.52868174, 0.29623892, 0.46701796,
                 0.78095718, 0.34553792, 0.63176220, 0.93348221, 0.83601751,
                 0.22793339, 0.19849637, 0.06926428, 0.12384706, 0.33956381]
            ]
        ]
    
    def test_getNumber(self):
        """
        Tests the implementation of the Wichmann-Hill algorithm concerning the
        mathematics.

        Test id: TEST-T-310
        Covers requirement: REQ-FUN-310

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        lstExpected = self.TestSets[0][1]
        for fItem in lstExpected:
            fTest = objTest.getNumber()
            self.assertIsInstance(fTest, float)
            self.assertAlmostEqual(fTest, fItem)
        for lstSeeds, lstExpected in self.TestSets:
            s1, s2, s3 = lstSeeds
            for _ in range(2):
                objTest.seed(s1, s2, s3)
                for fItem in lstExpected:
                    fTest = objTest.getNumber()
                    self.assertIsInstance(fTest, float)
                    self.assertAlmostEqual(fTest, fItem)
        del objTest

    def test_init_TypeError(self):
        """
        Tests that a sub-class of TypeError is raised if, at least, one of the
        allowed 3 optional seed values passed into the initialization method is
        not an integer number.

        Test id: TEST-T-311
        Covers requirement: REQ-AWM-300

        Version 1.0.0.0
        """
        for gItem in self.BadSeeds:
            with self.assertRaises(TypeError):
                self.TestClass(gItem)
            with self.assertRaises(TypeError):
                self.TestClass(1, gItem)
            with self.assertRaises(TypeError):
                self.TestClass(1, 1, gItem)
    
    def test_init_ValueError(self):
        """
        Tests that a sub-class of ValueError is raised if, at least, one of the
        allowed 3 optional seed values passed into the initialization method is
        an integer number but zero or negative.

        Test id: TEST-T-312
        Covers requirement: REQ-AWM-301

        Version 1.0.0.0
        """
        with self.assertRaises(ValueError):
            self.TestClass(0)
        with self.assertRaises(ValueError):
            self.TestClass(1, 0)
        with self.assertRaises(ValueError):
            self.TestClass(1, 1, 0)
        for _ in range(100):
            iSeed = - random.randint(1, 1000000000)
            with self.assertRaises(ValueError):
                self.TestClass(iSeed)
            with self.assertRaises(ValueError):
                self.TestClass(1, iSeed)
            with self.assertRaises(ValueError):
                self.TestClass(1, 1, iSeed)
    
    def test_seed_TypeError(self):
        """
        Tests that a sub-class of TypeError is raised if, at least, one of the
        3 seed values passed into the re-seeding method is not an integer
        number.

        Test id: TEST-T-311
        Covers requirement: REQ-AWM-300

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for gItem in self.BadSeeds:
            with self.assertRaises(TypeError):
                objTest.seed(gItem, 1, 1)
            with self.assertRaises(TypeError):
                objTest.seed(1, gItem, 1)
            with self.assertRaises(TypeError):
                objTest.seed(1, 1, gItem)
        del objTest
    
    def test_seed_ValueError(self):
        """
        Tests that a sub-class of ValueError is raised if, at least, one of the
        3 seed values passed into the re-seeding method is an integer number but
        zero or negative.

        Test id: TEST-T-312
        Covers requirement: REQ-AWM-301

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        with self.assertRaises(ValueError):
            objTest.seed(0, 1, 1)
        with self.assertRaises(ValueError):
            objTest.seed(1, 0, 1)
        with self.assertRaises(ValueError):
            objTest.seed(1, 1, 0)
        for _ in range(100):
            iSeed = - random.randint(1, 1000000000)
            with self.assertRaises(ValueError):
                objTest.seed(iSeed, 1, 1)
            with self.assertRaises(ValueError):
                objTest.seed(1, iSeed, 1)
            with self.assertRaises(ValueError):
                objTest.seed(1, 1, iSeed)
        del objTest

class Test_WH_Coder(unittest.TestCase):
    """
    Test cases for the the codecs_lib.wichmann_hill.WH_Coder class.
    
    Test ids: TEST-T-300, TEST-T-320, TEST-T-321, TEST-T-322, TEST-T-323,
    TEST-T-324
    Covered requirements: REQ-FUN-302, REQ-FUN-320, REQ-FUN-321, REQ-AWM-300,
    REQ-AWM-301, REQ-AWM-320

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version: 1.0.0.0
        """
        cls.TestClass = WH_Coder
        cls.Generator = WH_Generator
        cls.BadInput = [
            int, float, str, bytes, bytearray, '1', b'1', list, tuple, dict,
            ['1'], (1, '1'), [1, int], {1 : 1}]
        cls.BadSeeds = [1.0, int, float, str, bytes, bytearray, '1', b'1', list,
                        tuple, dict, [1], (1, 1), [1, int], {1 : 1}]
    
    def test_ContinuousOperation(self):
        """
        Checks that neither encoding nor decoding doesn't reset / re-seed the
        internal generator of the random numbers.

        Test id: TEST-T-300
        Covers requirement: REQ-FUN-302

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        objGenerator = self.Generator()
        for _ in range(10):
            lstInitial = []
            lstEncoded = []
            tupSeeds = (random.randint(1, 1000000000),
                        random.randint(1, 1000000000),
                        random.randint(1, 1000000000))
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            objGenerator.seed(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            iInput = random.randint(0, 100000)
            fOutput = objTest.encode(iInput)
            fCode = objGenerator.getNumber()
            fCheck = iInput / (fCode + 0.000001)
            self.assertAlmostEqual(fOutput, fCheck)
            lstInitial.append(iInput)
            lstEncoded.append(fOutput)
            iInput = random.randint(0, 100000)
            fOutput = objTest.decode(iInput)
            fCode = objGenerator.getNumber()
            fCheck = iInput * (fCode + 0.000001)
            self.assertAlmostEqual(fOutput, fCheck)
            lstInitial.append(iInput)
            lstEncoded.append(fOutput)
            lstTemp = []
            for _ in range(10):
                lstTemp.append(random.randint(1,1000))
                lstTemp.append(random.random())
            lstInitial.extend(lstTemp * 2)
            lstEncoded.extend(objTest.encode(lstTemp))
            lstEncoded.extend(objTest.decode(lstTemp))
            for _ in range(40):
                objGenerator.getNumber()
            fInput = random.randint(0, 1000) + random.random()
            fOutput = objTest.encode(fInput)
            fCode = objGenerator.getNumber()
            fCheck = fInput / (fCode + 0.000001)
            self.assertAlmostEqual(fOutput, fCheck)
            lstInitial.append(fInput)
            lstEncoded.append(fOutput)
            fInput = random.randint(0, 1000)
            fOutput = objTest.decode(fInput)
            fCode = objGenerator.getNumber()
            fCheck = fInput * (fCode + 0.000001)
            self.assertAlmostEqual(fOutput, fCheck)
            lstInitial.append(fInput)
            lstEncoded.append(fOutput)
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            lstDecoded = [objTest.decode(lstEncoded[0]),
                            objTest.encode(lstEncoded[1])]
            lstDecoded.extend(objTest.decode(lstEncoded[2 : 2 + len(lstTemp)]))
            lstDecoded.extend(objTest.encode(
                            lstEncoded[2 + len(lstTemp) : 2 + 2 *len(lstTemp)]))
            lstDecoded.extend([objTest.decode(lstEncoded[-2]),
                                                objTest.encode(lstEncoded[-1])])
            for iIndex, fDecoded in enumerate(lstDecoded):
                self.assertAlmostEqual(fDecoded, lstInitial[iIndex],
                                            msg = 'at index {}'.format(iIndex))
        del objTest
        del objGenerator

    def test_encode(self):
        """
        Checks the proper calculations by the encoding method.

        Test id: TEST-T-320
        Covers requirement: REQ-FUN-320

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        objGenerator = self.Generator()
        for _ in range(10):
            tupSeeds = (random.randint(1, 1000000000),
                        random.randint(1, 1000000000),
                        random.randint(1, 1000000000))
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            objGenerator.seed(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            for _ in range(1000):
                iInput = random.randint(0, 100000)
                fOutput = objTest.encode(iInput)
                fCode = objGenerator.getNumber()
                fCheck = iInput / (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fOutput = objTest.encode(-iInput)
                fCode = objGenerator.getNumber()
                fCheck = -iInput / (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fInput = random.randint(0, 100000) * random.random()
                fOutput = objTest.encode(fInput)
                fCode = objGenerator.getNumber()
                fCheck = fInput / (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fOutput = objTest.encode(-fInput)
                fCode = objGenerator.getNumber()
                fCheck = -fInput / (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
            lstGenerated = [random.randint(0, 100000) * random.random()
                                                            for _ in range(100)]
            lstGenerated.append(random.randint(1, 100000)) #make it mixed!
            lstOutput = objTest.encode(lstGenerated)
            self.assertIsInstance(lstOutput, list)
            for iIndex, fItem in enumerate(lstOutput):
                fInput = lstGenerated[iIndex]
                fCode = objGenerator.getNumber()
                fCheck = fInput / (fCode + 0.000001)
                self.assertIsInstance(fItem, float)
                self.assertAlmostEqual(fItem, fCheck)
            lstOutput = objTest.encode(tuple(lstGenerated))
            self.assertIsInstance(lstOutput, list)
            for iIndex, fItem in enumerate(lstOutput):
                fInput = lstGenerated[iIndex]
                fCode = objGenerator.getNumber()
                fCheck = fInput / (fCode + 0.000001)
                self.assertIsInstance(fItem, float)
                self.assertAlmostEqual(fItem, fCheck)
        del objTest
        del objGenerator
    
    def test_decode(self):
        """
        Checks the proper calculations by the encoding method.

        Test id: TEST-T-321
        Covers requirement: REQ-FUN-321

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        objGenerator = self.Generator()
        for _ in range(10):
            tupSeeds = (random.randint(1, 1000000000),
                        random.randint(1, 1000000000),
                        random.randint(1, 1000000000))
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            objGenerator.seed(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            for _ in range(1000):
                iInput = random.randint(0, 100000)
                fOutput = objTest.decode(iInput)
                fCode = objGenerator.getNumber()
                fCheck = iInput * (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fOutput = objTest.decode(-iInput)
                fCode = objGenerator.getNumber()
                fCheck = -iInput * (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fInput = random.randint(0, 100000) * random.random()
                fOutput = objTest.decode(fInput)
                fCode = objGenerator.getNumber()
                fCheck = fInput * (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
                fOutput = objTest.decode(-fInput)
                fCode = objGenerator.getNumber()
                fCheck = -fInput * (fCode + 0.000001)
                self.assertIsInstance(fOutput, float)
                self.assertAlmostEqual(fOutput, fCheck)
            lstGenerated = [random.randint(0, 100000) * random.random()
                                                            for _ in range(100)]
            lstGenerated.append(random.randint(1, 100000)) #make it mixed!
            lstOutput = objTest.decode(lstGenerated)
            self.assertIsInstance(lstOutput, list)
            for iIndex, fItem in enumerate(lstOutput):
                fInput = lstGenerated[iIndex]
                fCode = objGenerator.getNumber()
                fCheck = fInput * (fCode + 0.000001)
                self.assertIsInstance(fItem, float)
                self.assertAlmostEqual(fItem, fCheck)
            lstOutput = objTest.decode(tuple(lstGenerated))
            self.assertIsInstance(lstOutput, list)
            for iIndex, fItem in enumerate(lstOutput):
                fInput = lstGenerated[iIndex]
                fCode = objGenerator.getNumber()
                fCheck = fInput * (fCode + 0.000001)
                self.assertIsInstance(fItem, float)
                self.assertAlmostEqual(fItem, fCheck)
        del objTest
        del objGenerator

    def test_init_TypeError(self):
        """
        Tests that a sub-class of TypeError is raised if, at least, one of the
        allowed 3 optional seed values passed into the initialization method is
        not an integer number.

        Test id: TEST-T-322
        Covers requirement: REQ-AWM-300

        Version 1.0.0.0
        """
        for gItem in self.BadSeeds:
            with self.assertRaises(TypeError):
                self.TestClass(gItem)
            with self.assertRaises(TypeError):
                self.TestClass(1, gItem)
            with self.assertRaises(TypeError):
                self.TestClass(1, 1, gItem)
    
    def test_init_ValueError(self):
        """
        Tests that a sub-class of ValueError is raised if, at least, one of the
        allowed 3 optional seed values passed into the initialization method is
        an integer number but zero or negative.

        Test id: TEST-T-323
        Covers requirement: REQ-AWM-300

        Version 1.0.0.0
        """
        with self.assertRaises(ValueError):
            self.TestClass(0)
        with self.assertRaises(ValueError):
            self.TestClass(1, 0)
        with self.assertRaises(ValueError):
            self.TestClass(1, 1, 0)
        for _ in range(100):
            iSeed = - random.randint(1, 1000000000)
            with self.assertRaises(ValueError):
                self.TestClass(iSeed)
            with self.assertRaises(ValueError):
                self.TestClass(1, iSeed)
            with self.assertRaises(ValueError):
                self.TestClass(1, 1, iSeed)
    
    def test_seedGenerator_TypeError(self):
        """
        Tests that a sub-class of TypeError is raised if, at least, one of the
        3 seed values passed into the re-seeding method is not an integer
        number.

        Test id: TEST-T-322
        Covers requirement: REQ-AWM-300

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for gItem in self.BadSeeds:
            with self.assertRaises(TypeError):
                objTest.seedGenerator(gItem, 1, 1)
            with self.assertRaises(TypeError):
                objTest.seedGenerator(1, gItem, 1)
            with self.assertRaises(TypeError):
                objTest.seedGenerator(1, 1, gItem)
        del objTest
    
    def test_seedGenerator_ValueError(self):
        """
        Tests that a sub-class of ValueError is raised if, at least, one of the
        3 seed values passed into the re-seeding method is an integer number but
        zero or negative.

        Test id: TEST-T-323
        Covers requirement: REQ-AWM-301

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        with self.assertRaises(ValueError):
            objTest.seedGenerator(0, 1, 1)
        with self.assertRaises(ValueError):
            objTest.seedGenerator(1, 0, 1)
        with self.assertRaises(ValueError):
            objTest.seedGenerator(1, 1, 0)
        for _ in range(100):
            iSeed = - random.randint(1, 1000000000)
            with self.assertRaises(ValueError):
                objTest.seedGenerator(iSeed, 1, 1)
            with self.assertRaises(ValueError):
                objTest.seedGenerator(1, iSeed, 1)
            with self.assertRaises(ValueError):
                objTest.seedGenerator(1, 1, iSeed)
        del objTest

    def test_encode_TypeError(self):
        """
        Improper input data type for encoding results in an TypeError-type
        exception.

        Test id: TEST-T-324
        Covers requirement: REQ-AWM-320

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for gInput in self.BadInput:
            with self.assertRaises(TypeError):
                objTest.encode(gInput)
        for _ in range(100):
            tupSeeds = (random.randint(1, 1000000000),
                        random.randint(1, 1000000000),
                        random.randint(1, 1000000000))
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            for gInput in self.BadInput:
                with self.assertRaises(TypeError):
                    objTest.encode(gInput)
        del objTest
    
    def test_decode_TypeError(self):
        """
        Improper input data type for decoding results in an TypeError-type
        exception.

        Test id: TEST-T-324
        Covers requirement: REQ-AWM-320

        Version 1.0.0.0
        """
        objTest = self.TestClass()
        for gInput in self.BadInput:
            with self.assertRaises(TypeError):
                objTest.decode(gInput)
        for _ in range(100):
            tupSeeds = (random.randint(1, 1000000000),
                        random.randint(1, 1000000000),
                        random.randint(1, 1000000000))
            objTest.seedGenerator(tupSeeds[0], tupSeeds[1], tupSeeds[2])
            for gInput in self.BadInput:
                with self.assertRaises(TypeError):
                    objTest.decode(gInput)
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_WH_Generator)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_WH_Coder)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Testing codecs_lib.wichmann_hill module...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)