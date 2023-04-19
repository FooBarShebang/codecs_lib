#usr/bin/python3
"""
Module codecs_lib.cobs

Implementation of the Consistent Overhead Byte Stuffing (COBS) encoding and
decoding algorithm disregaring the packet delimiting b'\x00' characters.

References:
    [1] Wikipedia:
        https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing
    [2] Python implementation: https://pypi.org/project/cobs/
    [3] Cheshire, Stuart; Baker, Mary (April 1999)
        'Consistent Overhead Byte Stuffing'. IEEE/ACM Transactions on
        Networking. 7 (2): 159-172. CiteSeerX 10.1.1.108.3143.
        doi:10.1109/90.769765. Retrieved November 30, 2015.

Classes:
    COBS_Coder
"""

__version__ = "1.0.0.1"
__date__ = "19-04-2023"
__status__ = "Production"

#imports

#+ standard libraries

import os
import sys

from typing import Any, Union

#+ other DO libraries

LIB_FOLDER = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

TByteString = Union[bytes, bytearray]

#classes

class COBS_Coder:
    """
    Singleton-like class implementing Consistent Overhead Byte Stuffing (COBS)
    encoding / decoding algorithm disregaring the packet delimiting b'\x00'
    characters. All methods are class methods, thus the instantiation is not
    required, although it is possible.
    
    Class methods:
        decode(Data):
            bytes OR bytearray -> bytes
        encode(Data):
            bytes OR bytearray -> bytes
    
    Version 1.0.0.1
    """

    #private methods

    @classmethod
    def _checkType(cls, Data: Any) -> None:
        """
        Helper 'private' method to check that the input for encoding or decoding
        methods is a byte-string or a bytes array and raise a sub-class of
        TypeError exception if the check fails.

        Class method.

        Signature:
            type A -> None
        
        Args:
            Data: type A; the input of the encoding or decoding method to be
                checked
        
        Raises:
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.0.1
        """
        if not isinstance(Data, (bytes, bytearray)):
            raise UT_TypeError(Data, (bytes, bytearray), SkipFrames = 2)

    #public API

    @classmethod
    def encode(cls, Data: TByteString) -> bytes:
        """
        Encodes a byte string using COBS algorithm. Note that the frame
        delimiter b'\x00' is not added!

        Class method.
        
        Signature:
            bytes OR bytearray -> bytes
        
        Args:
            Data: bytes or bytearray; data to be encoded
        
        Returns:
            bytes: encoded byte-string
        
        Raises:
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.1.0
        """
        BlockLength = 254
        cls._checkType(Data)
        Segments = bytes(Data).split(b'\x00')
        Accumulator = bytearray()
        StopIndex = len(Segments) - 1
        for Index, Segment in enumerate(Segments):
            Length = len(Segment)
            if not Length:
                Accumulator.append(1)
            else:
                NumberParts = int(Length / BlockLength)
                BlocksLength = NumberParts * BlockLength
                for PartNumber in range(NumberParts):
                    Offset = PartNumber * BlockLength
                    Accumulator.append(255)
                    Accumulator.extend(Segment[Offset: Offset + BlockLength])
                BytesLeft = Length -  BlocksLength + 1
                if BytesLeft != 1:
                    Accumulator.append(BytesLeft)
                    Accumulator.extend(Segment[BlocksLength: ])
                elif Index < StopIndex: #package does not end with 254*(k>0)
                    # non-zero bytes
                    Accumulator.append(1)
        Result = bytes(Accumulator)
        return Result

    @classmethod
    def decode(cls, Data: TByteString) -> bytes:
        """
        Decodes a byte string using COBS algorithm. Note that the leading and
        tailing delimiters b'\x00' are removed automatically!
        
        Class method.
        
        Signature:
            bytes OR bytearray -> bytes
        
        Args:
            Data: bytes OR bytearray; data to be decoded
        
        Returns:
            bytes: decoded byte-string
        
        Raises:
            UT_ValueError: a zero character ('\x00') in the passed data not in
                the leading or tailing position
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.0.1
        """
        cls._checkType(Data)
        Input = bytes(Data).strip(b'\x00')
        if b'\x00' in Input:
            ErrorMessage = 'Zero character in the encoded string'
            raise UT_ValueError(Data, ErrorMessage, SkipFrames = 1)
        Input = bytearray(Input)
        Index = 0
        Result = bytearray()
        DataLength = len(Input)
        while (Index < DataLength):
            Code = Input[Index]
            Index += 1
            if Code > 1:
                Result.extend(Input[Index : Index + Code - 1])
                Index += Code - 1
            if (Code < 255) and (Index < DataLength):
                Result.append(0)
        Result = bytes(Result)
        return Result
