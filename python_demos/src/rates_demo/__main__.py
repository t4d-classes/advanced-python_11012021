""" rates demo """

from datetime import date

from rates_demo.business_days import business_days

if __name__ == "__main__":

    the_start_date = date(2020, 12, 15)
    the_end_date = date(2021, 1, 14)

    for business_day in business_days(the_start_date, the_end_date):
        print(business_day)
