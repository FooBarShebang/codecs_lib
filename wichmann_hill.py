#usr/bin/python3
"""
Module codecs_lib.wichmann_hill

Implementation of the encoding based on the modified Wichmann-Hill pseudo-random
numbers generator.

References:
    [1] Wikipedia: https://en.wikipedia.org/wiki/Wichmann%E2%80%93Hill

Classes:
    WH_Generator
    WH_Coder
"""

__version__ = "1.0.0.1"
__date__ = "19-04-2023"
__status__ = "Production"

#imports

#+ standard libraries

import os
import sys

from typing import Union, Sequence, List, Any
import collections.abc as c_abc
#import copy

#+ other DO libraries

LIB_FOLDER = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

T_REAL = Union[int, float]

T_REAL_SEQUENCE = Sequence[T_REAL]

T_INPUT_TYPE = Union[T_REAL, T_REAL_SEQUENCE]

T_OUTPUT_TYPE = Union[float, List[float]]

#functions - helpers

def _CheckSeed(s1: int, s2: int, s3: int) -> None:
    """
    'Private' helper function. Checks that all 3 arguments are positive
    integers; raises an exception on a failed test

    Sigature:
        int > 0, int > 0, int > 0 -> None
    
    Args:
        s1: int > 0; the first seed number to be checked
        s2: int > 0; the second seed number to be checked
        s3: int > 0; the third seed number to be checked
    
    Raises:
        UT_TypeError: any of the arguments is not an integer
        UT_ValueError: any of the arguments is a negative integer or zero
    
    Version 1.0.0.1
    """
    if (not isinstance(s1, int)) or isinstance(s1, bool):
        Error = UT_TypeError(s1, int, SkipFrames = 2)
        Error.appendMessage('- the first argument')
        raise Error
    elif s1 < 1:
        raise UT_ValueError(s1, 'positive integer - the first argument',
                                                                SkipFrames = 2)
    if (not isinstance(s2, int)) or isinstance(s2, bool):
        Error = UT_TypeError(s2, int, SkipFrames = 2)
        Error.appendMessage('- the second argument')
        raise Error
    elif s2 < 1:
        raise UT_ValueError(s2, 'positive integer - the second argument',
                                                                SkipFrames = 2)
    if (not isinstance(s3, int)) or isinstance(s3, bool):
        Error = UT_TypeError(s3, int, SkipFrames = 2)
        Error.appendMessage('- the third argument')
        raise Error
    elif s3 < 1:
        raise UT_ValueError(s3, 'positive integer - the third argument',
                                                                SkipFrames = 2)

#classes

class WH_Generator:
    """
    Implementation of a pseudo-random number generator in the range [0, 1) based
    on the modified Wichmann-Hill algorithm with strictly positive integer seeds
    at any time.

    Methods:
        seed(s1, s2, s3):
            int > 0, int > 0, int > 0 -> None
        getNumber():
            None -> 0 <= float < 1
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self, s1: int = 1, s2: int = 1, s3: int =1) -> None:
        """
        Initializer. Up to 3 positive integers can be supplied to be used as
        the seed values. By default the value 1 is used for each not supplied
        seed value.

        Sigature:
            /int > 0/, int > 0/, int > 0/// -> None
        
        Args:
            s1: (optional) int > 0; the first seed number to be used, defaults
                to 1
            s2: (optional) int > 0; the second seed number to be used, defaults
                to 1
            s3: (optional) int > 0; the third seed number to be used, defaults
                to 1
        
        Raises:
            UT_TypeError: any of the passed arguments is not an integer
            UT_ValueError: any of the passed arguments is a negative integer or
                zero
        
        Version 1.0.0.0
        """
        _CheckSeed(s1, s2, s3)
        self.seed(s1, s2, s3)
    
    #public API

    def seed(self, s1: int, s2: int, s3: int) -> None:
        """
        Method to change all 3 current seed values.

        Sigature:
            int > 0, int > 0, int > 0 -> None
        
        Args:
            s1: int > 0; the first seed number to be used
            s2: int > 0; the second seed number to be used
            s3: int > 0; the third seed number to be used
        
        Raises:
            UT_TypeError: any of the passed arguments is not an integer
            UT_ValueError: any of the passed arguments is a negative integer or
                zero
        
        Version 1.0.0.0
        """
        _CheckSeed(s1, s2, s3)
        self._s1 = s1
        self._s2 = s2
        self._s3 = s3
    
    def getNumber(self) -> float:
        """
        Updates the current seed values following the modified Wichmann-Hill
        algorithm, then calculates and returns a pseudo-random floating point
        number in the range [0, 1).

        Signature:
            None -> 0 <= float < 1
        
        Version 1.0.0.0
        """
        s1 = int(self._s1)
        s2 = int(self._s2)
        s3 = int(self._s3)
        self._s1 = (171 * (s1 % 177) - 2 * int(s1 / 177)) % 30269
        self._s2 = (172 * (s2 % 176) - 35 * int(s2 / 176)) % 30307
        self._s3 = (170 * (s3 % 178) - 63 * int(s3 / 178)) % 30323
        r = self._s1 / 30269 + self._s2 / 30307 + self._s3 / 30323
        Result = r - int(r)
        return Result

class WH_Coder:
    """
    Implementation of a coder / data scrambler based on the pseudo-random number
    generator in the range [0, 1) using the modified Wichmann-Hill algorithm -
    see WH_Generator class.

    Methods:
        seedGenerator(s1, s2, s3):
            int > 0, int > 0, int > 0 -> None
        encode(Data):
            int OR float OR seq(int OR float) -> float OR list(float)
        decode(Data):
            int OR float OR seq(int OR float) -> float OR list(float)
    
    Version 1.0.0.1
    """
    
    #special methods

    def __init__(self, s1: int = 1, s2: int = 1, s3: int =1) -> None:
        """
        Initializer. Up to 3 positive integers can be supplied to be used as
        the seed values in the internal WH generator. By default the value 1 is
        used for each not supplied seed value.

        Sigature:
            /int > 0/, int > 0/, int > 0/// -> None
        
        Args:
            s1: (optional) int > 0; the first seed number to be used, defaults
                to 1
            s2: (optional) int > 0; the second seed number to be used, defaults
                to 1
            s3: (optional) int > 0; the third seed number to be used, defaults
                to 1
        
        Raises:
            UT_TypeError: any of the passed arguments is not an integer
            UT_ValueError: any of the passed arguments is a negative integer or
                zero
        
        Version 1.0.0.1
        """
        _CheckSeed(s1, s2, s3)
        self._Codec = WH_Generator(s1, s2, s3)
    
    #private helper methods

    def _checkIfSequence(self, Data: Any) -> bool:
        """
        Private helper method to check if the passed data is a sequence, but not
        a Unicode or byte-string.

        Signature:
            type A -> bool
        
        Version 1.0.0.1
        """
        Cond1 = isinstance(Data, c_abc.Sequence)
        Cond2 = not isinstance(Data, str)
        Cond3 = not isinstance(Data, bytes)
        return Cond1 and Cond2 and Cond3
    
    def _checkIfNumber(self, Data: Any) -> bool:
        """
        Private helper method to check if the passed data is an integer or
        floating point number, but not a boolean value.

        Signature:
            type A -> bool
        
        Version 1.0.0.1
        """
        Cond1 = isinstance(Data, (int, float))
        Cond2 = not isinstance(Data, bool)
        return Cond1 and Cond2

    #public API

    def seedGenerator(self, s1: int, s2: int, s3: int) -> None:
        """
        Method to change all 3 current seed values within the internal pseudo-
        random numbers generator.

        Sigature:
            int > 0, int > 0, int > 0 -> None
        
        Args:
            s1: int > 0; the first seed number to be used
            s2: int > 0; the second seed number to be used
            s3: int > 0; the third seed number to be used
        
        Raises:
            UT_TypeError: any of the passed arguments is not an integer
            UT_ValueError: any of the passed arguments is a negative integer or
                zero
        
        Version 1.0.0.1
        """
        _CheckSeed(s1, s2, s3)
        self._Codec.seed(s1, s2, s3)

    def encode(self, Data: T_INPUT_TYPE) -> T_OUTPUT_TYPE:
        """
        Method to encode a single real number or a sequence of such numbers.

        Signature:
            int OR float OR seq(int OR float) -> float OR list(float)
        
        Args:
            Data: int OR float OR seq(int OR float); a real number or any
                sequence of real numbers to be encoded
        
        Returns:
            float; the encoded number - for a single number input
            list(float): the encoded numbers - for the sequence input
        
        Raises:
            UT_TypeError: the input is neither int, nor float, nor sequence of
                int or float
        
        Version 1.0.0.1
        """
        if self._checkIfSequence(Data):
            Result = []
            for Index, Item in enumerate(Data):
                if self._checkIfNumber(Item):
                    Code = self._Codec.getNumber()
                    Result.append(Item / (Code + 0.000001))
                    pass
                else:
                    Error = UT_TypeError(Item, (int, float), SkipFrames = 1)
                    Error.appendMessage(
                                    f'- at position {Index} in the sequence' )
                    raise Error
        elif self._checkIfNumber(Data):
            Code = self._Codec.getNumber()
            Result = Data / (Code + 0.000001)
            pass
        else:
            raise UT_TypeError(Data, (int, float, c_abc.Sequence), SkipFrames=1)
        return Result

    def decode(self, Data: T_INPUT_TYPE) -> T_OUTPUT_TYPE:
        """
        Method to decode a single real number or a sequence of such numbers.

        Signature:
            int OR float OR seq(int OR float) -> float OR list(float)
        
        Args:
            Data: int OR float OR seq(int OR float); a real number or any
                sequence of real numbers to be decoded
        
        Returns:
            float; the decoded number - for a single number input
            list(float): the decoded numbers - for the sequence input
        
        Raises:
            UT_TypeError: the input is neither int, nor float, nor sequence of
                int or float
        
        Version 1.0.0.1
        """
        if self._checkIfSequence(Data):
            Result = []
            for Index, Item in enumerate(Data):
                if self._checkIfNumber(Item):
                    Code = self._Codec.getNumber()
                    Result.append(Item * (Code + 0.000001))
                    pass
                else:
                    Error = UT_TypeError(Item, (int, float), SkipFrames = 1)
                    Error.appendMessage(
                                    f'- at position {Index} in the sequence')
                    raise Error
        elif self._checkIfNumber(Data):
            Code = self._Codec.getNumber()
            Result = Data * (Code + 0.000001)
            pass
        else:
            raise UT_TypeError(Data, (int, float, c_abc.Sequence), SkipFrames=1)
        return Result
