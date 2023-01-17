import asyncio

from nonebot import get_bot
from nonebot.log import logger

from plugins.scheduler_msg_queue import msg_queue

class BGTasks():
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.enabled_tasks = [
            'test'
        ]
        logger.debug('test')

    @property
    def bot(self):
        return get_bot()

    async def run(self):
        for task in self.enabled_tasks:
            await self.start_task(task)

    async def start_task(self, task_name):
        await self.loop.create_task(getattr(self, task_name)())

    async def test(self, interval=5):
        while True:
            logger.debug('test')
            await self.bot.send_group_msg(group_id=1014696092, message='test')
            await asyncio.sleep(interval)