#usr/bin/python3
"""
Module codecs_lib.xor_scrambler

Implementation of the per-byte XORing scrambling / unscrambling of the data.

Classes:
    XOR_Coder
"""

__version__ = "1.0.0.0"
__date__ = "30-06-2021"
__status__ = "Development"

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
    
    Version 1.0.0.0
    """
    
    #public API
    
    @classmethod
    def encode(cls, Data: TByteString, *,
                    Encoding: Optional[str] = None) -> bytes:
        """
        """
        pass
    
    @classmethod
    def decode(cls, Data: TBytes, *,
                    Encoding: Optional[str] = None) -> TString:
        """
        """
        pass