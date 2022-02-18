import asyncio
import json
import os.path
from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    token: Optional[str] = ''
    ignore_repos: Optional[list[Optional[str]]] = []

    class Config:
        extra = "ignore"


async def update_conf():
    global config
    path = './shigure'
    file_name = 'blackbe.json'
    full_path = os.path.join(path, file_name)

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(full_path):
        config = Config(**{'token': '', 'ignore_repos': []})
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(config.dict(), f)
    else:
        with open(full_path, encoding='utf-8') as f:
            config = Config(**json.load(f))


config = None
asyncio.run(update_conf())
