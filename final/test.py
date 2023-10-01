#!/usr/bin/env python3

from imgspy_asyncio import Imgspy
import asyncio

async def main():
    urls = ['http://via.placeholderssss.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    "/home/belovedtech/Downloads/6-Figure3-1.png",
    'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    "/home/belovedtech/Downloads/6-Figure3-1.png",
    "/home/belovedtech/Downloads/6-Figure3-1.png",
    'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    "/home/belovedtech/Downloads/6-Figure3-1.png","http://via.placeholder.com/1920x1080",
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    "/home/belovedtech/Downloads/6-Figure3-1.png",
    'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    "/home/belovedtech/Downloads/6aaaa-Figure3-1.pngsaaaaa",
    "/home/belovedtech/Downloads/6-Figure3-1.png",
    'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                'http://via.placeholder.com/1920x1080',
                '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''',
    '''data:image/png;base64,
    iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
    KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAEssdddlFTkSuQmCC''',
    "/home/belovedtech/Downloads/6-Figure3-1.png"]

    results = await Imgspy.info(*urls)
    print(results)


if __name__ == "__main__":

    asyncio.run(main())
