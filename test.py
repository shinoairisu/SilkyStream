import asyncio

async def lala():
    for i in range(100):
        print(i)
        await asyncio.sleep(0.01)

def xx():
    oop = asyncio.create_task(lala())
    print("你试试是是是是")
    oop2 = asyncio.create_task(lala())
    print("你试试是是是是")
    print("你试试是是是是")
    print("你试试是是是是")
    print("你试试是是是是")
    print("你试试是是是是")
    return oop,oop2


async def main():
    a,b = xx()
    await a
    await b

asyncio.run(main())