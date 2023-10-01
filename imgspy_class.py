# coding: utf-8
"""
imgspy asyncio
======

imgspy is a Python package designed for processing multiple image streams concurrently to extract their metadata, including image type, size, width, and height, based on their URLs. This package is built with asyncio, enabling efficient and parallel processing of image data. It is a Python implementation inspired by the `fastimage` library.

imgspy offers support for a variety of image types, including BMP, CUR, GIF, ICO, JPEG, PNG, PSD, TIFF, and WEBP.

.. _fastimage: https://github.com/sdsykes/fastimage

usage
-----
::

    >>> async def main():
        print((await imgspy.info(
            'http://via.placeholderssss.com/1920x1080',
            'http://via.placeholder.com/1920x1080',
            '''data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',)))

    asyncio.run(main())

    [None, {'type': 'png', 'width': 1920, 'height': 1080}, {'type': 'png', 'width': 1920, 'height': 1080}, {'type': 'png', 'width': 2, 'height': 1}]
"""
import io
import os
import sys
import base64
import struct
import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientError, http_exceptions
import logging

__version__ = '0.2.2'

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)


class OpenStream:
    def __init__(self, input: str):
        """
        Initialize the OpenStream object with the input source.

        Args:
            input (str): The input source, which can be a file path, URL, or data URI.
        """
        self.input = input
        self.__session = None
        self.logger = logging.getLogger(__class__.__name__)

    async def get_stream(self) -> io.BytesIO:
        """
        Get an asynchronous byte stream based on the input source.

        Returns:
            io.BytesIO: An asynchronous byte stream for further processing.
        """
        try:
            if hasattr(self.input, 'read'):
                return await self.__read_stream()
            elif os.path.isfile(self.input):
                return await self.__read_file()
            elif self.input.startswith('http'):
                return await self.__read_http()
            elif isinstance(self.input, str) and self.input.startswith('data:'):
                return await self.__read_data()
        except Exception as e:
            self.logger.error(f"Error while opening stream: {e}")

        finally:
            if self.__session:
                await self.__session.close()

    async def __read_file(self) -> io.BytesIO:
        """
        Read an input file and return it as an asynchronous byte stream.

        Returns:
            io.BytesIO: An asynchronous byte stream representing the file contents.
        """
        try:
            async with aiofiles.open(self.input, mode='rb') as f:
                return io.BytesIO(await f.read())
        except Exception as e:
            self.logger.error(f"Error while reading file: {e}")


    async def __read_http(self) -> io.BytesIO:
        """
        Read data from an HTTP URL and return it as an asynchronous byte stream.

        Returns:
            io.BytesIO: An asynchronous byte stream containing the HTTP response data.
        """
        try:
            if not self.__session:
                self.__session = aiohttp.ClientSession()
            async with self.__session.get(self.input) as response:
                if response.status == 200:
                    return io.BytesIO(await response.read())
                else:
                    self.logger.error(f"HTTP request failed with status code {response.status}")
                    Exception(f"HTTP request failed with status code {response.status}")
        except (ClientError, http_exceptions.HttpProcessingError) as e:
            self.logger.error(f"aiohttp exception for {self.input}: {e}",
            )
        except Exception as e:
            self.logger.error(f"Error while reading http: {e}")
            #

    async def __read_data(self) -> io.BytesIO:
        """
        Read data from a data URI and return it as an asynchronous byte stream.

        Returns:
            io.BytesIO: An asynchronous byte stream containing the data from the URI.
        """
        try:
            parts = self.input.split(';', 2)
            if len(parts) == 2 and parts[1].startswith('base64,'):
                return io.BytesIO(base64.b64decode(parts[1][7:]))
        except Exception as e:
            self.logger.error(f"Error while reading data: {e}")


    async def __read_stream(self) -> str:
        """
        Return the input source itself as a string.

        Returns:
            str: The input source string.
        """
        return self.input



class Probe(OpenStream):
    def __init__(self) -> None:
        """
        Initialize the Probe object with the input stream.

        Args:
            stream (io.BytesIO): An asynchronous byte stream.
        """
        self.stream = None
        self.chunk = None
        self.logger = logging.getLogger(__class__.__name__)

    async def get_info(self, input) -> dict:
        """
        Get the image metadata.

        Returns:
            dict: The image metadata.
        """
        try:
            self.stream = await OpenStream(input).get_stream()
            self.chunk = self.stream.read(26)
        except Exception as e:
            self.logger.error(f"Error while reading stream: {e}")
        else:
            if self.chunk.startswith(b'\x89PNG\r\n\x1a\n'):
                return self.__probe_png()
            elif self.chunk.startswith(b'GIF89a') or self.chunk.startswith(b'GIF87a'):
                return self.__probe_gif()
            elif self.chunk.startswith(b'\xff\xd8'):
                return self.__probe_jpeg()
            elif self.chunk.startswith(b'\x00\x00\x01\x00') or self.chunk.startswith(b'\x00\x00\x02\x00'):
                return self.__probe_ico()
            elif self.chunk.startswith(b'BM'):
                return self.__probe_bmp()
            elif self.chunk.startswith(b'MM\x00\x2a') or self.chunk.startswith(b'II\x2a\x00'):
                return self.__probe_tiff()
            elif self.chunk[:4] == b'\x00\x00\x00\x0c':
                return self.__probe_webp()
            elif self.chunk.startswith(b'8BPS'):
                return self.__probe_psd()


    def __probe_png(self) -> dict:
        """
        Probe a PNG image.

        Returns:
            dict: The image metadata.
        """
        try:
            if self.chunk[12:16] == b'IHDR':
                w, h = struct.unpack(">LL", self.chunk[16:24])
            elif self.chunk[12:16] == b'CgBI':
                self.chunk += self.stream.read(40 - len(self.chunk))
                w, h = struct.unpack('>LL', self.chunk[32:40])
            else:
                w, h = struct.unpack(">LL", self.chunk[8:16])
            return {'type': 'png', 'width': w, 'height': h}
        except Exception as e:
            self.logger.error(f"Error while probing PNG: {e}")


    def __probe_gif(self) -> dict:
        """
        Probe a GIF image.

        Returns:
            dict: The image metadata.
        """
        try:
            w, h = struct.unpack('<HH', self.chunk[6:10])
            return {'type': 'gif', 'width': w, 'height': h}
        except Exception as e:
            self.logger.error(f"Error while probing GIF: {e}")


    def __probe_jpeg(self) -> dict:
        """
        Probe a JPEG image.

        Returns:
            dict: The image metadata.
        """
        try:
            start = 2
            data = self.chunk
            while True:
                if data[start:start+1] != b'\xff':
                    return
                if data[start+1] in b'\xc0\xc2':
                    h, w = struct.unpack('>HH', data[start+5:start+9])
                    return {'type': 'jpg', 'width': w, 'height': h}
                segment_size, = struct.unpack('>H', data[start+2:start+4])
                data += self.stream.read(segment_size + 9)
                start = start + segment_size + 2
        except Exception as e:
            self.logger.error(f"Error while probing JPEG: {e}")


    def __probe_ico(self):
        """
        Probe an ICO image.

        Returns:
            dict: The image metadata.
        """
        try:
            img_type = 'ico' if self.chunk[2:3] == b'\x01' else 'cur'
            num_images = struct.unpack('<H', self.chunk[4:6])[0]
            w, h = struct.unpack('BB', self.chunk[6:8])
            w = 256 if w == 0 else w
            h = 256 if h == 0 else h
            return {'type': img_type, 'width': w, 'height': h, 'num_images': num_images}
        except Exception as e:
            self.logger.error(f"Error while probing ICO: {e}")


    def __probe_bmp(self):
        """
        Probe a BMP image.

        Returns:
            dict: The image metadata.
        """
        try:
            headersize = struct.unpack("<I", self.chunk[14:18])[0]
            if headersize == 12:
                w, h = struct.unpack("<HH", self.chunk[18:22])
            elif headersize >= 40:
                w, h = struct.unpack("<ii", self.chunk[18:26])
            else:
                return
            return {'type': 'bmp', 'width': w, 'height': h}
        except Exception as e:
            self.logger.error(f"Error while probing BMP: {e}")


    def __probe_tiff(self):
        """
        Probe a TIFF image.

        Returns:
            dict: The image metadata.
        """
        try:
            w, h, orientation = None, None, None

            endian = '>' if self.chunk[0:2] == b'MM' else '<'
            offset = struct.unpack(endian + 'I', self.chunk[4:8])[0]
            self.chunk += self.stream.read(offset - len(self.chunk) + 2)

            tag_count = struct.unpack(endian + 'H', self.chunk[offset:offset+2])[0]
            offset += 2
            for i in range(tag_count):
                if len(self.chunk) - offset < 12:
                    self.chunk += self.stream.read(12)
                type = struct.unpack(endian + 'H', self.chunk[offset:offset+2])[0]
                data = struct.unpack(endian + 'H', self.chunk[offset+8:offset+10])[0]
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
        except Exception as e:
            self.logger.error(f"Error while probing TIFF: {e}")


    def __probe_webp(self):
        """
        Probe a WEBP image.

        Returns:
            dict: The image metadata.
        """
        try:
            w, h = None, None
            type = self.chunk[15:16]
            self.chunk += self.stream.read(30 - len(self.chunk))
            if type == b' ':
                w, h = struct.unpack('<HH', self.chunk[26:30])
                w, h = w & 0x3fff, h & 0x3fff
            elif type == b'L':
                w = 1 + (((ord(self.chunk[22:23]) & 0x3F) << 8) | ord(self.chunk[21:22]))
                h = 1 + (((ord(self.chunk[24:25]) & 0xF) << 10) |
                         (ord(self.chunk[23:24]) << 2) | ((ord(self.chunk[22:23]) & 0xC0) >> 6))
            elif type == b'X':
                w = 1 + struct.unpack('<I', self.chunk[24:27] + b'\x00')[0]
                h = 1 + struct.unpack('<I', self.chunk[27:30] + b'\x00')[0]
            return {'type': 'webp', 'width': w, 'height': h}
        except Exception as e:
            self.logger.error(f"Error while probing WEBP: {e}")


    def __probe_psd(self):
        """
        Probe a PSD image.

        Returns:
            dict: The image metadata.
        """
        try:
            h, w = struct.unpack('>LL', self.chunk[14:22])
            return {'type': 'psd', 'width': w, 'height': h}
        except Exception as e:
            self.logger.error(f"Error while probing PSD: {e}")




async def info(*input):
    return await asyncio.gather(*[processor(i) for i in input])


async def processor(input):
    return await Probe().get_info(input)
