""" py thread """

import time
import threading

mydata = threading.local()

def python_is_fun():
    print("python_is_fun", mydata.msg)


def do_it(msg: str, msg2: str) -> None:
    """ do it """
    time.sleep(1)
    print("did it", msg, msg2)
    mydata.msg = msg
    python_is_fun()

thread1 = threading.Thread(
    target=do_it, args=("thread1","maps are cool"))
thread1.start()

thread2 = threading.Thread(
    target=do_it, args=("thread2","geospatial stuff is awesome"))
thread2.start()

thread1.join()
thread2.join()


print("made it here")


