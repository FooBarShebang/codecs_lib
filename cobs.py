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

__version__ = "1.0.0.0"
__date__ = "17-06-2021"
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
        decode(bData):
            bytes OR bytearray -> bytes
        encode(bData):
            bytes OR bytearray -> bytes
    
    Version 1.0.0.0
    """

    #private methods

    @classmethod
    def _checkType(cls, gData: Any) -> None:
        """
        Helper 'private' method to check that the input for encoding or decoding
        methods is a byte-string or a bytes array and raise a sub-class of
        TypeError exception if the check fails.

        Class method.

        Signature:
            type A -> None
        
        Args:
            gData: type A; the input of the encoding or decoding method to be
                checked
        
        Raises:
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.0.0
        """
        if not isinstance(gData, (bytes, bytearray)):
            raise UT_TypeError(gData, (bytes, bytearray), SkipFrames = 2)

    #public API

    @classmethod
    def encode(cls, bData: TByteString) -> bytes:
        """
        Encodes a byte string using COBS algorithm. Note that the frame
        delimiter b'\x00' is not added!

        Class method.
        
        Signature:
            bstring -> bstring
        
        Args:
            bsInput: bytes or bytearray; data to be encoded
        
        Returns:
            bytes: encoded byte-string
        
        Raises:
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.0.0
        """
        cls._checkType(bData)
        bslstBuffer = bytes(bData).split(b'\x00')
        baTemp = bytearray()
        iBigLen = len(bslstBuffer) - 1
        for iBigIndex, bsTemp in enumerate(bslstBuffer):
            iLen = len(bsTemp)
            if not iLen:
                baTemp.append(1)
            else:
                iParts = int(iLen / 254)
                for iIndex in range(iParts):
                    baTemp.append(255)
                    baTemp.extend(bsTemp[iIndex * 254 : (iIndex + 1) * 254])
                iRemainderLen = iLen - iParts * 254 + 1
                if iRemainderLen != 1:
                    baTemp.append(iRemainderLen)
                    baTemp.extend(bsTemp[iParts * 254 : iLen])
                elif iBigIndex < iBigLen: #package does not end with 254*(k>0)
                    # non-zero bytes
                    baTemp.append(1)
        bsResult = bytes(baTemp)
        return bsResult

    @classmethod
    def decode(cls, bData: TByteString) -> bytes:
        """
        Decodes a byte string using COBS algorithm. Note that the leading and
        tailing delimiters b'\x00' are removed automatically!
        
        Class method.
        
        Signature:
            bytes OR bytearray -> bytes
        
        Args:
            bData: bytes OR bytearray; data to be decoded
        
        Returns:
            bytes: decoded byte-string
        
        Raises:
            UT_ValueError: a zero character ('\x00') in the passed data not in
                the leading or tailing position
            UT_TypeError: input is neither byte-string nor bytes array
        
        Version 1.0.0.0
        """
        cls._checkType(bData)
        bsBuffer = bytes(bData).strip(b'\x00')
        if b'\x00' in bsBuffer:
            strError = 'Zero character in the encoded string'
            raise UT_ValueError(bData, strError, SkipFrames = 1)
        baBuffer = bytearray(bsBuffer)
        iIndex = 0
        baResult = bytearray()
        iLen = len(baBuffer)
        while (iIndex < iLen):
            iCode = baBuffer[iIndex]
            iIndex += 1
            if iCode > 1:
                baResult.extend(bsBuffer[iIndex : iIndex + iCode - 1])
                iIndex += iCode - 1
            if (iCode < 255) and (iIndex < iLen):
                baResult.append(0)
        bsResult = bytes(baResult)
        return bsResult
