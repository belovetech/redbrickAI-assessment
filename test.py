from imgspy import info
import time
import asyncio


def main():
    start_time = time.perf_counter()
    for _ in range(10):
        print(info('http://via.placeholder.com/1920x1080'))
        print(info('http://via.placeholder.com/1920x1080'))
        print(info('http://via.placeholder.com/1920x1080'))
        print(info('''data:image/png;base64,
            iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
            KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC'''))
        print(info('''data:image/png;base64,
        iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
        KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC'''))
    elapsed = time.perf_counter() - start_time
    print(f"Elapsed {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    main()
