import asyncio

async def producer(queue:asyncio.Queue):
    for i in range(100):
        await queue.put(i)
        await asyncio.sleep(1e-3)
        print("塞入一个元素")

async def consumer(queue):
    for i in range(100):
        x = await queue.get()
        print(x)
    # n = 0
    # while True:
    #     res = await queue.get()
    #     print(res)

async def main():
    x = asyncio.Queue(maxsize=10)
    await asyncio.gather(producer(x),consumer(x))

asyncio.run(main())