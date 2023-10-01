FROM python:3.9-slim

RUN pip install aiohttp aiofiles

COPY ./imgspy_asyncio.py imgspy_asyncio.py

COPY ./test2.py test2.py

CMD ["python", "test2.py"]
