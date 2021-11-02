""" py thread """

import time
import threading


def do_it(msg: str, msg2: str) -> None:
    """ do it """
    #time.sleep(1)
    print("did it", msg, msg2)

thread1 = threading.Thread(
    target=do_it, args=("thread1","maps are cool"))
thread1.start()

thread2 = threading.Thread(
    target=do_it, args=("thread2","geospatial stuff is awesome"))
thread2.start()


print("made it here")


