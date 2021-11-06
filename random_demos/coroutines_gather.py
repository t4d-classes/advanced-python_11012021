import asyncio
from random import randint
import threading

def delay() -> float:
    """ delay """
    return float(randint(1,10) / 2)

async def get_data(task_num: int) -> None:
    """ get data """
    print(f"starting get data {task_num} {threading.get_ident()}")
    await asyncio.sleep(delay())
    print(f"finished get data {task_num} {threading.get_ident()}")



async def main():

    await asyncio.gather(get_data(1), get_data(2), get_data(3))


asyncio.run(main())

