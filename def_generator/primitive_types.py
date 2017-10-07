#!/usr/bin/python
# coding=utf-8
from struct import unpack
from StringIO import StringIO

__author__ = "Aleksandr Shyshatsky"


def BLOB(stream):
    """
    BLOB — Size (bytes): N+k
    Binary data. Similar to a string, but can contain NULL characters.
    Stored in base-64 encoding when in XML, e.g., in the XML database.
    N is the number of bytes in the blob, and k=4.
    :type stream: StringIO
    :rtype: object 
    """
    size, = unpack('B', stream.read(1))
    # hack for arenaStateReceived
    if size == 0xff:
        size, = unpack('H', stream.read(2))
        # some dummy shit
        unpack('B', stream.read(1))

        result = stream.read(size)
        return result,
    return stream.read(size),


def STRING(stream):
    """
    STRING — Size (bytes): N+k
    Binary string data. 
    :type stream: StringIO
    :rtype: object 
    """
    size, = unpack('B', stream.read(1))
    return stream.read(size),


def PYTHON(stream):
    """
    BLOB — Size (bytes): N+k
    Binary data. Similar to a string, but can contain NULL characters.
    Stored in base-64 encoding when in XML, e.g., in the XML database.
    N is the number of bytes in the blob, and k=4.
    :type stream: StringIO
    :rtype: object 
    """
    size, = unpack('B', stream.read(1))
    return stream.read(size),


def FLOAT32(stream):
    """
    FLOAT32 — Size (bytes): 4
    IEEE 32-bit floating-point number.
    :type stream: StringIO
    :rtype: float 
    """
    return unpack('f', stream.read(4))


def FLOAT64(stream):
    """
    FLOAT64 — Size (bytes): 8
    IEEE 64-bit floating-point number.
    :type stream: StringIO
    :rtype: float 
    """
    return unpack('d', stream.read(4))


def INT8(stream):
    """
    INT8 — Size (bytes): 1 — Range: From: -128 To: 127
    Signed 8-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('b', stream.read(1))

def INT16(stream):
    """
    INT16 — Size (bytes): 2 — Range: From: -32,768 To: 32,767
    Signed 16-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('h', stream.read(2))


def INT32(stream):
    """
    INT32 — Size (bytes): 4 — Range: From: -2,147,483,648 To: 2,147,483,647
    Signed 32-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('i', stream.read(4))


def INT64(stream):
    """
    INT64 — Size (bytes): 8 — Range: From: -9,223,372,036,854,775,808 To: 9,223,372,036,854,775,807
    Signed 64-bit integer.
    :type stream: StringIO
    :rtype: long 
    """
    return unpack('q', stream.read(8))


def UINT8(stream):
    """
    UINT8 — Size(bytes): 1 - Range: From: 0 To: 255
    Unsigned 8-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('B', stream.read(1))

def UINT16(stream):
    """
    UINT16 — Size(bytes): 2 — Range: From: 0 To: 65,535
    Unsigned 16-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('H', stream.read(2))


def UINT32(stream):
    """
    UINT32 — Size(bytes): 4 — Range: From: 0 To: 4,294,967,295
    Unsigned 32-bit integer.
    :type stream: StringIO
    :rtype: int 
    """
    return unpack('I', stream.read(4))


def UINT64(stream):
    """
    UINT64 — Size(bytes): 8 — Range: From: 0 To: 18,446,744,073,709,551,615
    Unsigned 64-bit integer.
    :type stream: StringIO
    :rtype: long 
    """
    return unpack('Q', stream.read(8))


def MAILBOX(stream):
    """
    MAILBOX — Size (bytes): 12
    A BigWorld mailbox.
    Passing an entity to a MAILBOX argument automatically converts it to MAILBOX.
    :type stream: StringIO
    :rtype: object  
    """
    raise NotImplemented()


def VECTOR2(stream):
    """VECTOR2 — Size(bytes): 8
    Two-dimensional vector of 32-bit floats. Represented in Python as a tuple of two numbers (or Math.Vector2).
    """
    return unpack('ff', stream.read(8)),


def VECTOR3(stream):
    """VECTOR3 — Size(bytes): 12
    Three-dimensional vector of 32-bit floats. Represented in Python as a tuple of three numbers (or Math.Vector3).
    """
    return unpack('fff', stream.read(12)),


def VECTOR4(stream):
    """VECTOR4 — Size(bytes): 16
    Four-dimensional vector of 32-bit floats. Represented in Python as a tuple of four numbers (or Math.Vector4).
    """
    return unpack('ffff', stream.read(16)),

TYPES = {
    'BLOB': BLOB,
    'STRING': STRING,
    'UNICODE_STRING': STRING,
    'FLOAT': FLOAT32,
    'FLOAT32': FLOAT32,
    'FLOAT64': FLOAT64,
    'INT8': INT8,
    'INT16': INT16,
    'INT32': INT32,
    'INT64': INT64,
    'UINT8': UINT8,
    'UINT16': UINT16,
    'UINT32': UINT32,
    'UINT64': UINT64,
    'VECTOR2': VECTOR2,
    'VECTOR3': VECTOR3,
    'VECTOR4': VECTOR4,
    'PYTHON': PYTHON
}