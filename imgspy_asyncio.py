# coding: utf-8
"""
imgspy
======

imgspy finds the metadata (type, size) of an image given its url by fetching
as little as needed. This is a python implementation of `fastimage`_. Supports
image types BMP, CUR, GIF, ICO, JPEG, PNG, PSD, TIFF, WEBP.

.. _fastimage: https://github.com/sdsykes/fastimage

usage
-----

::

    >>> imgspy.info('http://via.placeholder.com/1920x1080')
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> with requests.get('http://via.placeholder.com/1920x1080', stream=True) as res:
    ...     imgspy.info(res.raw)
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> imgspy.info('/path/to/image.jpg')
    {'type': 'jpg', 'width': 420, 'height': 240}
    >>> with open('/path/to/image.jpg') as f:
    ...     imgspy.info(f)
    {'type': 'jpg', 'width': 420, 'height': 240}
"""
import io
import os
import sys
import base64
import struct
import asyncio
import aiohttp
from aiohttp import ClientError, http_exceptions
import aiofiles

__version__ = '0.2.2'


async def openstream(input):
    try:
        if hasattr(input, 'read'):
            return input
        elif os.path.isfile(input):
            start_time = time.perf_counter()
            async with aiofiles.open(input, mode='rb') as f:
                res = io.BytesIO(await f.read())
            elapsed = time.perf_counter() - start_time
            print(f"OPEN file took {elapsed:0.2f} seconds.")
            return res
        elif input.startswith('http'):
            start_time = time.perf_counter()
            async with aiohttp.ClientSession() as session:
                async with session.get(input) as response:
                    res = io.BytesIO(await response.read())
            elapsed = time.perf_counter() - start_time
            print(f"HTTP took {elapsed:0.2f} seconds.")
            return res
        elif isinstance(input, str) and input.startswith('data:'):
            parts = input.split(';', 2)
            if len(parts) == 2 and parts[1].startswith('base64,'):
                return io.BytesIO(base64.b64decode(parts[1][7:]))
    except Exception as e:
        print(e.me)
        sys.exit(1)


async def info(*input):
    result = await asyncio.gather(*[processor(i) for i in input])
    return result


import time

async def processor(input):
    stream = await openstream(input)
    return probe(stream)



def probe(stream):
    chunk = stream.read(26)

    if chunk.startswith(b'\x89PNG\r\n\x1a\n'):
        return probe_png(chunk, stream)
    elif chunk.startswith(b'GIF89a') or chunk.startswith(b'GIF87a'):
        return probe_gif(chunk)
    elif chunk.startswith(b'\xff\xd8'):
        return probe_jpeg(chunk, stream)
    elif chunk.startswith(b'\x00\x00\x01\x00') or chunk.startswith(b'\x00\x00\x02\x00'):
        return probe_unknown_type(chunk)
    elif chunk.startswith(b'BM'):
        return probe_bmp(chunk)
    elif chunk.startswith(b'MM\x00\x2a') or chunk.startswith(b'II\x2a\x00'):
        return probe_tiff(chunk, stream)
    elif chunk[:4] == b'RIFF' and chunk[8:15] == b'WEBPVP8':
        return probe_webp(chunk, stream)
    elif chunk.startswith(b'8BPS'):
        return probe_psd(chunk)

def probe_png(chunk, stream):
    if chunk[12:16] == b'IHDR':
        w, h = struct.unpack(">LL", chunk[16:24])
    elif chunk[12:16] == b'CgBI':
        chunk += stream.read(40 - len(chunk))
        w, h = struct.unpack('>LL', chunk[32:40])
    else:
        w, h = struct.unpack(">LL", chunk[8:16])
    return {'type': 'png', 'width': w, 'height': h}


def probe_gif(chunk):
    w, h = struct.unpack('<HH', chunk[6:10])
    return {'type': 'gif', 'width': w, 'height': h}


def probe_jpeg(chunk, stream):
    start = 2
    data = chunk
    while True:
        if data[start:start+1] != b'\xff':
            return
        if data[start+1] in b'\xc0\xc2':
            h, w = struct.unpack('>HH', data[start+5:start+9])
            return {'type': 'jpg', 'width': w, 'height': h}
        segment_size, = struct.unpack('>H', data[start+2:start+4])
        data += stream.read(segment_size + 9)
        start = start + segment_size + 2


def probe_unknown_type(chunk):
    img_type = 'ico' if chunk[2:3] == b'\x01' else 'cur'
    num_images = struct.unpack('<H', chunk[4:6])[0]
    w, h = struct.unpack('BB', chunk[6:8])
    w = 256 if w == 0 else w
    h = 256 if h == 0 else h
    return {'type': img_type, 'width': w, 'height': h, 'num_images': num_images}


def probe_bmp(chunk):
    headersize = struct.unpack("<I", chunk[14:18])[0]
    if headersize == 12:
        w, h = struct.unpack("<HH", chunk[18:22])
    elif headersize >= 40:
        w, h = struct.unpack("<ii", chunk[18:26])
    else:
        return
    return {'type': 'bmp', 'width': w, 'height': h}


def probe_tiff(chunk, stream):
    w, h, orientation = None, None, None

    endian = '>' if chunk[0:2] == b'MM' else '<'
    offset = struct.unpack(endian + 'I', chunk[4:8])[0]
    chunk += stream.read(offset - len(chunk) + 2)

    tag_count = struct.unpack(endian + 'H', chunk[offset:offset+2])[0]
    offset += 2
    for i in range(tag_count):
        if len(chunk) - offset < 12:
            chunk += stream.read(12)
        type = struct.unpack(endian + 'H', chunk[offset:offset+2])[0]
        data = struct.unpack(endian + 'H', chunk[offset+8:offset+10])[0]
        offset += 12
        if type == 0x100:
            w = data
        elif type == 0x101:
            h = data
        elif type == 0x112:
            orientation = data
        if all([w, h, orientation]):
            break

    if orientation >= 5:
        w, h = h, w
    return {'type': 'tiff', 'width': w, 'height': h, 'orientation': orientation}


def probe_webp(chunk, stream):
    w, h = None, None
    type = chunk[15:16]
    chunk += stream.read(30 - len(chunk))
    if type == b' ':
        w, h = struct.unpack('<HH', chunk[26:30])
        w, h = w & 0x3fff, h & 0x3fff
    elif type == b'L':
        w = 1 + (((ord(chunk[22:23]) & 0x3F) << 8) | ord(chunk[21:22]))
        h = 1 + (((ord(chunk[24:25]) & 0xF) << 10) |
                 (ord(chunk[23:24]) << 2) | ((ord(chunk[22:23]) & 0xC0) >> 6))
    elif type == b'X':
        w = 1 + struct.unpack('<I', chunk[24:27] + b'\x00')[0]
        h = 1 + struct.unpack('<I', chunk[27:30] + b'\x00')[0]
    return {'type': 'webp', 'width': w, 'height': h}


def probe_psd(chunk):
    h, w = struct.unpack('>LL', chunk[14:22])
    return {'type': 'psd', 'width': w, 'height': h}


