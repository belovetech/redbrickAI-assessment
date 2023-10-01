import io
import os
import sys
import base64
import struct
import asyncio
import aiohttp
import aiofiles
import logging
from urllib.parse import urlparse

__version__ = '0.2.2'

# Constants for chunk sizes
PNG_HEADER_SIZE = 26
JPEG_HEADER_SIZE = 2
WEBP_HEADER_SIZE = 30
TIFF_HEADER_SIZE = 8
PSD_HEADER_SIZE = 22


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)




def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.error(f"Invalid input: {e}")
        raise

async def open_stream(input):
    try:
        is_valid_url(input)
        if hasattr(input, 'read'):
            return input
        elif os.path.isfile(input):
            async with aiofiles.open(input, mode='rb') as f:
                return io.BytesIO(await f.read())
        elif input.startswith('http'):
            async with aiohttp.ClientSession() as session:
                async with session.get(input) as response:
                    return io.BytesIO(await response.read())
        elif isinstance(input, str) and input.startswith('data:'):
            parts = input.split(';', 2)
            if len(parts) == 2 and parts[1].startswith('base64,'):
                return io.BytesIO(base64.b64decode(parts[1][7:]))
    except Exception as e:
        logger.error(f"Error while opening stream: {e}")
        raise

async def info(*inputs):
    try:
        results = await asyncio.gather(*[processor(i) for i in inputs])
        return results
    except Exception as e:
        logger.error(f"Error in info function: {e}")
        raise

async def processor(input):
    try:
        stream = await open_stream(input)
        return await probe(stream)
    except Exception as e:
        logger.error(f"Error in processor function: {e}")
        raise

async def struct_unpack(format, value):
    return struct.unpack(format, value)


async def probe(stream):
    try:
        chunk = stream.read(PNG_HEADER_SIZE)

        if chunk.startswith(b'\x89PNG\r\n\x1a\n'):
            return await probe_png(chunk, stream)
        elif chunk.startswith(b'GIF89a') or chunk.startswith(b'GIF87a'):
            return await probe_gif(chunk)
        elif chunk.startswith(b'\xff\xd8'):
            return await probe_jpeg(chunk, stream)
        elif chunk.startswith(b'\x00\x00\x01\x00') or chunk.startswith(b'\x00\x00\x02\x00'):
            return await probe_unknown_type(chunk)
        elif chunk.startswith(b'BM'):
            return await probe_bmp(chunk)
        elif chunk.startswith(b'MM\x00\x2a') or chunk.startswith(b'II\x2a\x00'):
            return await probe_tiff(chunk, stream)
        elif chunk[:4] == b'RIFF' and chunk[8:15] == b'WEBPVP8':
            return await probe_webp(chunk, stream)
        elif chunk.startswith(b'8BPS'):
            return await probe_psd(chunk)
    except Exception as e:
        logger.error(f"Error in probe function: {e}")
        raise

async def probe_png(chunk, stream):
    try:
        if chunk[12:16] == b'IHDR':
            w, h = await struct_unpack(">LL", chunk[16:24])
        elif chunk[12:16] == b'CgBI':
            chunk += stream.read(40 - len(chunk))
            w, h = await struct_unpack('>LL', chunk[32:40])
        else:
            w, h = await struct_unpack(">LL", chunk[8:16])
        return {'type': 'png', 'width': w, 'height': h}
    except Exception as e:
        logger.error(f"Error in probe_png function: {e}")
        raise

async def probe_gif(chunk):
    try:
        w, h = await struct_unpack('<HH', chunk[6:10])
        return {'type': 'gif', 'width': w, 'height': h}
    except Exception as e:
        logger.error(f"Error in probe_gif function: {e}")
        raise

async def probe_jpeg(chunk, stream):
    try:
        start = JPEG_HEADER_SIZE
        data = chunk
        while True:
            if data[start:start+1] != b'\xff':
                return
            if data[start+1] in b'\xc0\xc2':
                h, w = await struct_unpack('>HH', data[start+5:start+9])
                return {'type': 'jpg', 'width': w, 'height': h}
            segment_size, = await struct_unpack('>H', data[start+2:start+4])
            data += stream.read(segment_size + 9)
            start = start + segment_size + 2
    except Exception as e:
        logger.error(f"Error in probe_jpeg function: {e}")
        raise

async def probe_unknown_type(chunk):
    try:
        img_type = 'ico' if chunk[2:3] == b'\x01' else 'cur'
        num_images = await struct_unpack('<H', chunk[4:6])[0]
        w, h = await struct_unpack('BB', chunk[6:8])
        w = 256 if w == 0 else w
        h = 256 if h == 0 else h
        return {'type': img_type, 'width': w, 'height': h, 'num_images': num_images}
    except Exception as e:
        logger.error(f"Error in probe_unknown_type function: {e}")
        raise

async def probe_bmp(chunk):
    try:
        headersize = await struct_unpack("<I", chunk[14:18])[0]
        if headersize == 12:
            w, h = await struct_unpack("<HH", chunk[18:22])
        elif headersize >= 40:
            w, h = await struct_unpack("<ii", chunk[18:26])
        else:
            return
        return {'type': 'bmp', 'width': w, 'height': h}
    except Exception as e:
        logger.error(f"Error in probe_bmp function: {e}")
        raise

async def probe_tiff(chunk, stream):
    try:
        w, h, orientation = None, None, None

        endian = '>' if chunk[0:2] == b'MM' else '<'
        offset = await struct_unpack(endian + 'I', chunk[4:8])[0]
        chunk += stream.read(offset - len(chunk) + TIFF_HEADER_SIZE)

        tag_count = await struct_unpack(endian + 'H', chunk[offset:offset+2])[0]
        offset += 2
        for i in range(tag_count):
            if len(chunk) - offset < 12:
                chunk += stream.read(12)
            type = await struct_unpack(endian + 'H', chunk[offset:offset+2])[0]
            data = await struct_unpack(endian + 'H', chunk[offset+8:offset+10])[0]
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
        return
    except Exception as e:
        logger.error(f"Error in probe_bmp function: {e}")
        raise

async def probe_webp(chunk, stream):
    try:
        w, h = None, None
        type = chunk[15:16]
        chunk += stream.read(30 - len(chunk))
        if type == b' ':
            w, h = await struct_unpack('<HH', chunk[26:30])
            w, h = w & 0x3fff, h & 0x3fff
        elif type == b'L':
            w = 1 + (((ord(chunk[22:23]) & 0x3F) << 8) | ord(chunk[21:22]))
            h = 1 + (((ord(chunk[24:25]) & 0xF) << 10) |
                    (ord(chunk[23:24]) << 2) | ((ord(chunk[22:23]) & 0xC0) >> 6))
        elif type == b'X':
            w = 1 + await struct_unpack('<I', chunk[24:27] + b'\x00')[0]
            h = 1 + await struct_unpack('<I', chunk[27:30] + b'\x00')[0]
        return {'type': 'webp', 'width': w, 'height': h}
    except Exception as e:
        logger.error(f"Error in probe_webp function: {e}")
        raise

async def probe_psd(chunk):
    try:
        h, w = await struct_unpack('>LL', chunk[14:22])
        return {'type': 'psd', 'width': w, 'height': h}
    except Exception as e:
        logger.error(f"Error in probe_psd function: {e}")
        raise


