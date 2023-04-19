#usr/bin/python3
"""
Module codecs_lib.xor_scrambler

Implementation of the per-byte XORing scrambling / unscrambling of the data.

Classes:
    XOR_Coder
"""

__version__ = "1.0.0.1"
__date__ = "19-04-2023"
__status__ = "Production"

#imports

#+ standard libraries

import os
import sys

from typing import Union, Optional

#+ other DO libraries

LIB_FOLDER = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

TBytes = Union[bytes, bytearray]

TByteString = Union[bytes, bytearray, str]

TString = Union[bytes, str]

#classes

class XOR_Coder:
    """
    Singleton-like class implementing per-byte XOR based scrambling and
    unscrambling. All methods are class methods, thus the instantiation is not
    required, although it is possible.
    
    Class methods:
        encode(Data, *, Encoding = None):
            bytes OR bytearray OR str\, *, str OR None\ -> bytes
        decode(Data *, Encoding = None):
            bytes OR bytearray\, *, str OR None\ -> bytes OR str
    
    Version 1.0.0.1
    """
    
    #public API
    
    @classmethod
    def encode(cls, Data: TByteString, *,
                    Encoding: Optional[str] = None) -> bytes:
        """
        Encodes the input into a byte string using per byte XOR with 255. If the
        input is a string and Encoding is not specified or None the UTF8 is
        assumed, otherwise the specified codec is used, which must be registred
        with Python.
        
        Signature:
            bytes OR bytearray OR str\, *, str OR None\ -> bytes
        
        Args:
            Data: bytes OR bytearray OR str; data to be encoded
            Encoding: (keyword only) str OR None; name of the Unicode codec to
                be used, None defaults to UTF8
        
        Returns:
            bytes: encoded byte string
        
        Raises:
            * UT_TypeError: Data is neither bytes nor bytearray nor string, OR
                Encoding is neither a string nor None if Data is a string
            * UT_ValueError: Encoding is not a registered, OR registered but
                improper codec - only if Data is a string
        
        Version 1.0.0.1
        """
        if isinstance(Data, bytes):
            Temp = bytearray(Data)
        elif isinstance(Data, bytearray):
            Temp = Data
        elif isinstance(Data, str):
            if Encoding is None:
                _Encoding = 'utf-8'
            elif not isinstance(Encoding, str):
                raise UT_TypeError(Encoding, str, SkipFrames = 1)
            else:
                _Encoding = Encoding
            try:
                Temp = Data.encode(_Encoding)
            except LookupError:
                raise UT_ValueError(Encoding,
                        'a registered Unicode codec', SkipFrames = 1) from None
            except ValueError:
                raise UT_ValueError(Encoding,
                        'a suitable Unicode codec', SkipFrames = 1) from None
            Temp = bytearray(Temp)
        else:
            raise UT_TypeError(Data, (bytes, bytearray, str), SkipFrames = 1)
        Result = bytes(Item ^ 255 for Item in Temp)
        return Result
    
    @classmethod
    def decode(cls, Data: TBytes, *,
                    Encoding: Optional[str] = None) -> TString:
        """
        Decodes the input into a byte string using per byte XOR with 255. If the
        Encoding is specified and not None it is used to decode the result into
        a string; the codec must be registred with Python.
        
        Signature:
            bytes OR bytearray\, *, str OR None\ -> bytes OR str
        
        Args:
            Data: bytes OR bytearray; data to be decoded
            Encoding: (keyword only) str OR None; name of the Unicode codec to
                be used, default value None prevents bytes -> str conversion
        
        Returns:
            * bytes: decoded byte string, Encoding is not specified or None
            * str: decoded byte string additionaly decoded into a Unicode, only
                if a valid string Encoding value is provided
        
        Raises:
            * UT_TypeError: Data is neither bytes nor bytearray, OR Encoding is
                not a string nor None
            * UT_ValueError: Encoding is not a registered, OR registered but
                improper codec
        
        Version 1.0.0.1
        """
        if isinstance(Data, bytes):
            Temp = bytearray(Data)
        elif isinstance(Data, bytearray):
            Temp = Data
        else:
            raise UT_TypeError(Data, (bytes, bytearray), SkipFrames = 1)
        Result = bytes(Item ^ 255 for Item in Temp)
        if not (Encoding is None):
            if not isinstance(Encoding, str):
                raise UT_TypeError(Encoding, str, SkipFrames = 1)
            try:
                Result = Result.decode(Encoding)
            except LookupError:
                raise UT_ValueError(Encoding,
                        'a registered Unicode codec', SkipFrames = 1) from None
            except ValueError:
                raise UT_ValueError(Encoding,
                        'a suitable Unicode codec', SkipFrames = 1) from None
        return Result