import json
import aiofiles
from typing import Union

async def read_json(path: str):
    async with aiofiles.open(path, 'rb') as f:
        data = await json.load(f)
    return data

async def write_json(path: str, data: Union[dict, list]):
    async with aiofiles.open(path, 'w') as f:
        await json.dump(data, f)

async def read_txt(path: str):
    async with aiofiles.open(path, 'r') as f:
        data = await f.read()
    return data