""" py thread """

import time
import threading


def do_it() -> None:
    """ do it """
    #time.sleep(1)
    print("did it")

thread1 = threading.Thread(target=do_it, args=tuple())
thread1.start()

thread2 = threading.Thread(target=do_it, args=tuple())
thread2.start()


print("made it here")


