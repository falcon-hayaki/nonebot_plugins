import asyncio

async def test():
    while True:
        print('test')
        await asyncio.sleep(2)

async def main():
    while True:
        print('main')
        await asyncio.sleep(3)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(test())
    loop.run_until_complete(main())