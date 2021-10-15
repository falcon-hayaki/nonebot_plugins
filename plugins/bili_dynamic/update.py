from typing import Awaitable
from os.path import join

from utils import fileio
from .main import resource_path
from database import mongo
from plugins.scheduler_msg_queue import msg_queue

class UpdateDyanamic():
    def __init__(self) -> None:
        self.db = mongo.dynamic

    async def init_data(self):
        self.subscribe = await fileio.read_json(join(resource_path, 'subscribes.json'))

    async def run(self):
        for uid in self.subscribe:
            if not list(self.db.find({"_id": uid})):
                pass

    async def insert_new(self, uid):
        pass