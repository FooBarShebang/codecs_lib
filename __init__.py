#!/usr/bin/python3
"""
Library codecs_lib

Collection of simple codecs for data manipulation as re-packaging and
scrambling. This library may be used against accidental disclosure of the
sensitive data, but it is not designed for use as an actual cryptography tool.

Modules:
    cobs: cyclic (circular) list based implementation of the Consistent Overhead
        Byte Stuffing, e.g. for the serial port communication
    vigenere: simple data per-byte encryption / decription using multiple-table
        substition Vigenere cipher method
    wichmann_hill: simple data encryption / decription using arithmetic
        operations with pseudo-random numbers generated by a modified
        Wichmann-Hill algorithm generator
    xor_scrambler: simple data scrambler using per-byte XORing with 0xFF (255d)
"""

__project__ = 'Python data manipulation codecs'
__version_info__= (1, 0, 1)
__version_suffix__= '-rc1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '19-04-2023'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['cobs', 'vigenere', 'wichmann_hill', 'xor_scrambler']