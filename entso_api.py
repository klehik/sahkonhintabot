from datetime import timedelta, datetime
import os
from DataItem import Day, Timespan

def get_day(date: datetime):
    
    start = datetime(date.year, date.month, date.day, 0)
    one_day = timedelta(days=1)
    data_item = Day(start=start, end=start+one_day, days=1)
    data_item.init_data_item()

    return data_item

def get_7(end: datetime):
    one_week = timedelta(days=7)
    
    data_item = Timespan(start=end-one_week, end=end, days=7)
    data_item.init_data_item()

    return data_item

def get_28(end: datetime):
    one_month = timedelta(days=28)
    
    data_item = Timespan(start=end-one_month, end=end, days=28)
    data_item.init_data_item()

    return data_item
