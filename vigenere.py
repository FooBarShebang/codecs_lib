#usr/bin/python3
"""
Module codecs_lib.vigenere

Implementation of the encoding based on the extended Vigenere cipher with the
mod 256.

References:
    [1] Wikipedia:
        https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

Classes:
    CircularList
    VigenereCoder
"""

__version__ = "1.0.0.0"
__date__ = "27-07-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import os
import sys

from typing import Any, Union, Sequence, Optional
import collections.abc as c_abc
import copy

#+ other DO libraries

LIB_FOLDER = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError
from introspection_lib.base_exceptions import UT_Exception

#+ types

T_BYTES = Union[bytes, bytearray]

T_PASSWORD = Union[bytes, bytearray, str]

#classes

class CircularList:
    """
    Implementation of an indefinite, repetitive feeder based on a circular list,
    where one element at a time is returned with each call to the method
    getElement(), and all elements of the stored sequence are iterated in an
    indefinite looping with wrapping from the end to the beginning of the
    sequence.

    Methods:
        setContent(seqData):
            seq(type A) -> None
        resetCounter():
            None -> None
        getElement():
            None -> type A
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self, seqData: Optional[Sequence[Any]] = None) -> None:
        """
        Initializer. Sets the internal counter to zero. Optionally sets the
        content of the container, if a proper sequence type is passed.

        Signature:
            /seq(type A)/ -> None
        
        Args:
            seqData: (optional) seq(type A); any sequence of any elements, the
                content to be stored, defaults to None, in which case the
                container is initially emtpy, and its content must be set
                explicitely before use
        
        Raises:
            UT_TypeError: the passed optional argument is neither None nor a
                sequence type
            UT_ValueError: the passed optional argument is an empty sequence
        
        Version 1.0.0.0
        """
        self._iCounter = 0
        self._seqData = None
        if not (seqData is None):
            if not isinstance(seqData, c_abc.Sequence):
                raise UT_TypeError(seqData, c_abc.Sequence, SkipFrames = 1)
            if not len(seqData):
                raise UT_ValueError(seqData, 'not empty sequence', SkipFrames=1)
            self.setContent(seqData)

    #public API

    def setContent(self, seqData: Sequence[Any]) -> None:
        """
        Copies and strores the passed sequence content into the internal buffer
        to be used as the data feed source.

        Signature:
            seq(type A) -> None
        
        Args:
            seqData: seq(type A); any sequence of any elements, the content to
                be stored
        
        Raises:
            UT_TypeError: the argument is not a sequence type
            UT_ValueError: the argument is an empty sequence
        """
        if not isinstance(seqData, c_abc.Sequence):
            raise UT_TypeError(seqData, c_abc.Sequence, SkipFrames = 1)
        if not len(seqData):
            raise UT_ValueError(seqData, 'not empty sequence', SkipFrames = 1)
        self._seqData = copy.deepcopy(seqData)
        self._iCounter = 0

    def resetCounter(self) -> None:
        """
        Resets the internal counter (pointer to an element) to zero.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self._iCounter = 0

    def getElement(self) -> Any:
        """
        Returns the current element of the stored content and increments the
        internal counter. Upon reaching the last element of the stored content
        the internal counter is automatically reset to zero.

        Signature:
            None -> type A
        
        Raises:
            UT_Exception: the stored content is not yet set

        Version 1.0.0.0
        """
        if self._seqData is None:
            raise UT_Exception('content is not yet set', SkipFrames = 1)
        gElement = self._seqData[self._iCounter]
        self._iCounter += 1
        if self._iCounter == len(self._seqData):
            self._iCounter = 0
        return gElement

class VigenereCoder:
    """
    Implementation of a codec based on the extended (mod 256) Vigenere
    substituion algorithm using cyclic pass-phrase. The pass-phrase can be set
    during instantiation or later using the dedicated method as a bytestring,
    bytes array or a string (Unicode), in the last case the string is
    automatically converted into a bytestring using UTF-8 codec. The pass-phrase
    must be set before the first encoding or decoding attempt.

    The internal index for the cyclic pass-phrase is never implicitely reset.
    Use the dedicated method explicitely or (re-) set the pass-phrase to reset
    the internal index. With this approach the codec is appropriate for the
    continuous data feed, e.g. for an input stream.

    Methods:
        setPassword(Password):
            str OR bytes OR bytearray -> None
        resetIndex():
            None -> None
        encode(Data, *, Codec):
            str/, *, str OR None/ -> bytes
        decode(Data, *, Codec):
            bytes OR bytearray/, *, str OR None/ -> str
    
    Version 1.0.0.0
    """
    
    #special methods

    def __init__(self, Password: Optional[T_PASSWORD] = None) -> None:
        """
        Initializer. If the optional Password argument is passed (and not None)
        the pass-phrase is also set. The passed string is converted into a
        bytestring using UTF-8 codec.

        Signature:
            /str OR bytes OR bytearray OR None/-> None
        
        Args:
            Password: (optional) str OR bytes OR bytearray OR None; pass-phrase
                to be set, unless None value (default) is passed, in which case
                the pass-phrase is not set.
        
        Raises:
            UT_TypeError: the passed argument is neither string, nor bytes
                array, nor bytestring, nor None
        
        Version 1.0.0.0
        """
        self._objCodec = None
        if not (Password is None):
            self._checkPassword(Password)
            self.setPassword(Password)
    
    #'private' helper methods

    def _checkPassword(self, Password: T_PASSWORD) -> None:
        """
        Helper method to check the validity of the type of the provided pass-
        phrase. Raises a custom version of TypeError if the check fails.

        Signature:
            str OR bytes OR bytearray -> None
        
        Args:
            Password: str OR bytes OR bytearray; pass-phrase to be checked
        
        Raises:
            UT_TypeError: the passed argument is neither string, nor bytes
                array, nor bytestring
        
        Version 1.0.0.0
        """
        if not isinstance(Password, (str, bytes, bytearray)):
            raise UT_TypeError(Password, (str, bytes, bytearray), SkipFrames= 2)

    #public API

    def setPassword(self, Password: T_PASSWORD) -> None:
        """
        Method to set the pass-phrase to be used in encoding and decoding. The
        passed string is converted into a bytestring using UTF-8 codec.

        Signature:
            str OR bytes OR bytearray -> None
        
        Args:
            Password: str OR bytes OR bytearray; pass-phrase to be checked
        
        Raises:
            UT_TypeError: the passed argument is neither string, nor bytes
                array, nor bytestring
        
        Version 1.0.0.0
        """
        self._checkPassword(Password)
        if isinstance(Password, bytearray):
            PassPhrase = copy.copy(Password)
        elif isinstance(Password, bytes):
            PassPhrase = bytearray(Password)
        else:
            PassPhrase = bytearray(Password, 'utf_8')
        if self._objCodec is None:
            self._objCodec = CircularList(PassPhrase)
        else:
            self._objCodec.setContent(PassPhrase)

    def resetIndex(self) -> None:
        """
        Method to reset the internal index to the beginning of the pass-phrase.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        if not (self._objCodec is None):
            self._objCodec.resetCounter()

    def encode(self, Data: str, *, Codec: Optional[str] = None) -> bytes:
        """
        Encodes the data passed as a string (Unicode) using the already set
        pass-phrase and the specified Unicode codec (if not provided UTF-8 is
        used by default).

        Signature:
            str/, *, str OR None/ -> bytes
        
        Args:
            Data: str; data to be encoded
            Codec: (keyword) str OR None; name of the Unicode codec to use for
                the str -> bytes conversion, if None or not indicated - the
                default UTF-8 is used
        
        Returns:
            bytes: the Vignere encoded data
        
        Raises:
            UT_TypeError: passed mandatory argument is not a string, OR the
                passed keyword argument is not a string or None
            UT_ValueError: the requested Unicode codec is not registered or
                incompatible with the passed data string
            UT_Exception: the pass-phrase is not set yet
        
        Version 1.0.0.0
        """
        if self._objCodec is None:
            raise UT_Exception('Pass-phrase is not set yet', SkipFrames = 1)
        if not isinstance(Data, str):
            raise UT_TypeError(Data, str, SkipFrames = 1)
        if Codec is None:
            _Codec = 'utf_8'
        else:
            if not isinstance(Codec, str):
                raise UT_TypeError(Codec, str, SkipFrames = 1)
            _Codec = Codec
        try:
            InData = bytearray(Data, _Codec)
        except LookupError:
            raise UT_ValueError(_Codec,
                        'a registered Unicode codec', SkipFrames = 1) from None
        except ValueError:
            raise UT_ValueError(_Codec,
                        'a suitable Unicode codec', SkipFrames = 1) from None
        OutData = bytes(bytearray((InByte + self._objCodec.getElement()) % 256 
                                                        for InByte in InData))
        return OutData

    def decode(self, Data: T_BYTES, *, Codec: Optional[str] = None) -> str:
        """
        Decodes the data passed as a bytestring or bytes array using the already
        set pass-phrase and the specified Unicode codec (if not provided UTF-8
        is used by default).

        Signature:
            bytes OR bytearray /, *, str OR None/ -> str
        
        Args:
            Data: bytes OR bytearray; data to be decoded
            Codec: (keyword) str OR None; name of the Unicode codec to use for
                the bytes -> str conversion, if None or not indicated - the
                default UTF-8 is used
        
        Returns:
            bytes: the Vignere encoded data
        
        Raises:
            UT_TypeError: passed mandatory argument is not a bytestring or bytes
                array, OR the passed keyword argument is not a string or None
            UT_ValueError: the requested Unicode codec is not registered or
                incompatible with the Vigenere decoded bytestring
            UT_Exception: the pass-phrase is not set yet
        
        Version 1.0.0.0
        """
        if self._objCodec is None:
            raise UT_Exception('Pass-phrase is not set yet', SkipFrames = 1)
        if not isinstance(Data, (bytes, bytearray)):
            raise UT_TypeError(Data, (bytes, bytearray), SkipFrames = 1)
        if Codec is None:
            _Codec = 'utf_8'
        else:
            if not isinstance(Codec, str):
                raise UT_TypeError(Codec, str, SkipFrames = 1)
            _Codec = Codec
        if isinstance(Data, bytearray):
            InData = Data
        else:
            InData = bytearray(Data)
        try:
         OutData = bytearray((InByte - self._objCodec.getElement()) % 256 
                                            for InByte in InData).decode(_Codec)
        except LookupError:
            raise UT_ValueError(_Codec,
                        'a registered Unicode codec', SkipFrames = 1) from None
        except ValueError:
            raise UT_ValueError(_Codec,
                        'a suitable Unicode codec', SkipFrames = 1) from None
        return OutData
