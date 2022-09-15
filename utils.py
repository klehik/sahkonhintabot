import os
from datetime import datetime, timedelta

def format_price(value):
    price = round(value, 2)
    price = format(price, '.2f')
    return price


     