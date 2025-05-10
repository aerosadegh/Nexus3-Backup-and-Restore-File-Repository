import asyncio


class Repository:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_item(self, item):
        await self.queue.put(item)
        return item

    async def pop_item(self):
        return await self.queue.get()
