import multiprocessing as mp
from multiprocessing.sharedctypes import Synchronized


def increment_process_count(process_count):

    with process_count.get_lock():
        process_count.value += 1
        print(process_count.value)


def run():

    process_count: Synchronized = mp.Value('i', 0)

    increment_processes = []

    for x in range(8):
        the_process = mp.Process(
            target=increment_process_count, args=(process_count,))
        the_process.start()
        increment_processes.append(the_process)

    for p in increment_processes:
        p.join()


    print("process count", process_count.value)

if __name__ == "__main__":
    run()



