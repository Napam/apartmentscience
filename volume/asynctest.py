import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.create_task(say_after(2, "world")), asyncio.create_task(say_after(1, "hello"))
    )

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
