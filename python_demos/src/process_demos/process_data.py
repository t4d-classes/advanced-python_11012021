""" process data """

import multiprocessing as mp

process_count = 0

def increment_process_count():

    global process_count

    process_count += 1
    print(process_count)


def run():

    increment_processes = []

    for x in range(8):
        the_process = mp.Process(target=increment_process_count)
        the_process.start()
        increment_processes.append(the_process)

    for p in increment_processes:
        p.join()


    print("process count", process_count)

if __name__ == "__main__":
    run()