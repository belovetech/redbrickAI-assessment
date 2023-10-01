import unittest
import asyncio
from imgspy_asyncio import OpenStream, Imgspy
from unittest.mock import patch, MagicMock


class TestOpenStream(unittest.TestCase):

    def test_file_stream(self):
        input_path = 'path/to/invalid-file-path'
        stream = asyncio.run(OpenStream(input_path)._get_stream())
        self.assertIsNone(stream)

    def test_http_stream(self):
        input_url = 'http://via.placeholder.com/1920x1080'
        stream = asyncio.run(OpenStream(input_url)._get_stream())
        self.assertIsNotNone(stream)
        self.assertTrue(isinstance(stream.read(), bytes))

    def test_data_stream(self):
        input_data_uri = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC'
        stream = asyncio.run(OpenStream(input_data_uri)._get_stream())
        self.assertIsNotNone(stream)
        self.assertTrue(isinstance(stream.read(), bytes))



class TestImgspy(unittest.TestCase):

    @patch('Iimgspy_asyncio.Probe')
    @patch('asyncio.gather')
    async def test_info(self, mock_gather, mock_probe):
        mock_probe.return_value.get_info.return_value = [{'type': 'png', 'width': 1920, 'height': 1080}, {'type': 'png', 'width': 1920, 'height': 1080}, None]
        mock_gather.return_value = [MagicMock(), MagicMock()]

        input_urls = ['http://via.placeholder.com/1920x1080', 'http://via.placeholder.com/1920x1080' 'http://invalid-url']
        results = await Imgspy.info(*input_urls)

        self.assertTrue(mock_gather.called)
        self.assertEqual(len(results), len(input_urls))
        for result in results:
            self.assertIsInstance(result, dict)
            self.assertEqual(result, [{'type': 'png', 'width': 1920, 'height': 1080}, {'type': 'png', 'width': 1920, 'height': 1080}, None])


if __name__ == "__main__":
    unittest.main()
