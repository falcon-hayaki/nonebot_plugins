from motor.motor_asyncio import AsyncIOMotorClient

class Mongo():
    def __init__(self, uri=None) -> None:
        if uri:
            self.db = AsyncIOMotorClient(uri)
        else:
            self.db = AsyncIOMotorClient("mongodb://127.0.0.1:27017/nonebot")