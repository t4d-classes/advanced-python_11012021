""" py thread """

import threading


def do_it() -> None:
    """ do it """
    #time.sleep(1)
    print("did it")
    print(threading.get_ident())
    print(threading.current_thread().name)

def run() -> None:
    """ run """

    thread1 = threading.Thread(target=do_it, name="thread1", args=tuple())
    thread1.start()

    thread2 = threading.Thread(target=do_it, name="thread2", args=tuple())
    thread2.start()


    print("made it here")


if __name__ == "__main__":
    run()
