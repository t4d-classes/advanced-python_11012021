import asyncio
from random import randint

def delay():
    """ delay """
    return randint(1,10) / 2

async def get_data(task_num: int) -> None:
    """ get data """
    print(f"starting get data {task_num}")
    await asyncio.sleep(delay())
    print(f"finished get data {task_num}")



async def main():

    await get_data(1)


asyncio.run(main())

