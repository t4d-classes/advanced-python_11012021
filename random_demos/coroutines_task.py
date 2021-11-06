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

    task1 = asyncio.create_task(get_data(1))
    task2 = asyncio.create_task(get_data(2))
    task3 = asyncio.create_task(get_data(3))

    await task1
    await task2
    await task3


asyncio.run(main())

