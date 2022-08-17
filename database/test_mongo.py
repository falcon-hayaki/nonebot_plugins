import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class Mongo():
    def __init__(self, uri=None) -> None:
        if uri:
            self.db = AsyncIOMotorClient(uri).nonebot
        else:
            self.db = AsyncIOMotorClient("mongodb://127.0.0.1:27017").nonebot

class TestMongoClient():
    def __init__(self):
        mongo = Mongo()
        self.db = mongo.db.test_collection
    
    async def find(self):
        cursor = self.db.find({'_id': 'test_2'})
        for res in await cursor.to_list(length=100):
            print(res, type(res))
    
    async def insert(self, data):
        if isinstance(data, dict):
            data = [data]
        res = await self.db.insert_many(data)
        print(res)
    
if __name__ == "__main__":
    client = TestMongoClient()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(client.insert({'_id': 'test_2', 'b': 'b'}))
    loop.run_until_complete(client.find())    