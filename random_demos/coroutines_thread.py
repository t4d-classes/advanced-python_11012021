import asyncio
from random import randint
import threading
import time

def delay():
    """ delay """
    return randint(1,10) / 2

def get_data_sync(task_num: int) -> None:
    """ get data """
    print(f"thread id: {threading.get_ident()}")
    print(f"starting get data {task_num}")
    time.sleep(delay()) # place holder for sync io operation
    print(f"finished get data {task_num}")

async def get_data_async(task_num: int) -> None:
    """ get data """
    print(f"thread id: {threading.get_ident()}")
    print(f"starting get data {task_num}")
    await asyncio.sleep(delay()) # place holder for async io operation
    print(f"finished get data {task_num}")



async def main():

    # get_data_sync(1)
    # get_data_sync(2)
    # get_data_sync(3)

    await asyncio.gather(
        asyncio.to_thread(get_data_sync, 1),
        asyncio.to_thread(get_data_sync, 2),
        asyncio.to_thread(get_data_sync, 3),
    )

    # task1 = asyncio.create_task(get_data_async(1))
    # task2 = asyncio.create_task(get_data_async(2))
    # task3 = asyncio.create_task(get_data_async(3))

    # await task1
    # await task2
    # await task3


asyncio.run(main())

