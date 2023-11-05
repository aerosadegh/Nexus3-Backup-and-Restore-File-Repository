import asyncio
from enum import Enum


class Color(str, Enum):
    GREEN = r"\x1b[32m"
    RESET = r"\x1b[39m"
    RED = r"\x1b[31m"
    BLUE = r"\x1b[34m"


class Repository:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_item(self, item):
        await self.queue.put(item)
        try:
            items_info = item["pypi"]
            print(f"{Color.GREEN}>>>>{Color.RESET} {items_info['name']}_{items_info['version']}")
        except KeyError:
            pass

    async def pop_item(self):
        item = await self.queue.get()
        try:
            items_info = item["pypi"]
            print(f"{Color.RED}<<<<{Color.RESET} {items_info['name']}_{items_info['version']}")
        except KeyError:
            pass
        return item
