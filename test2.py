#!/usr/bin/env python3

from imgspy_class import imgspy
import asyncio
import time


async def main():
    start_time = time.perf_counter()
    print(await imgspy.info('http://via.placeholderssss.com/1920x1080',
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
    "/home/belovedtech/Downloads/6-Figure3-1.png"))

    elapsed = time.perf_counter() - start_time
    print(f"Elapsed {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    # import imgspy_class
    # from imgspy_class import imgspy


    async def main():
        print(await imgspy.info('http://via.placeholder.com/1920x1080'))


    asyncio.run(main())
