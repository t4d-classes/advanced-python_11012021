""" dates demo """

from datetime import date, datetime, timedelta
import time

def run_demo() -> None:
    """ run demo """

    start_time = time.time()

    print("dates demo")

    start = datetime.now()
    end = start + timedelta(days=180)

    print(end)

    time.sleep(2)

    print(end - start)

    # print(type(start))
    # print(type(timedelta(days=180)))

    # print(start)
    # print(end)

    # print(type(1))
    # print(type('0.1'))
    # print(1 + '0.1')

    independence_day = date(1776, 7, 4)

    print(independence_day)
    print(type(independence_day))

    print(datetime.now().strftime("%B %A"))

    tax_day_str = "05-2021-17"

    tax_day = datetime.strptime(tax_day_str, "%m-%Y-%d")

    print(tax_day)

    if datetime.now() > tax_day:
        print("tax day has passed, hope you paid your taxes")
    else:
        print("tax day is coming up, better get busy filling out the forms")

    end_time = time.time()

    print(end_time - start_time)


    print(datetime.now().weekday())

    


