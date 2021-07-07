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
__date__ = "07-07-2021"
__status__ = "Development"

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
    """
    pass