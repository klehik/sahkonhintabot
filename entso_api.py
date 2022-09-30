from datetime import timedelta, datetime
import os

from matplotlib.pyplot import title
from DataItem import Day, Timespan
import calendar
from utils import get_month_name, get_days_in_month

def get_day(date: datetime):
    
    start = datetime(date.year, date.month, date.day, 0)
    one_day = timedelta(days=1)
    title = f""
    data_item = Day(start=start, end=start+one_day, title=title)
    data_item.init_data_item()

    return data_item

def get_week(date):
    # +1 days = today
    date = datetime(date.year, date.month, date.day)
    end = date + timedelta(days=1)
    start = end - timedelta(days=7)
    title = f"Pörssisähkön 7 vrk:n tuntihinnat"
    data_item = Timespan(start=start, end=end, title=title)
    data_item.init_data_item()

    return data_item

def get_28(end: datetime):
    one_month = timedelta(days=28)
    title = f"Pörssisähkön 28 vrk:n keskihinnat"
    data_item = Timespan(start=end-one_month, end=end, title=title)
    data_item.init_data_item()

    return data_item

def get_month(date):

    start = datetime(date.year, date.month, 1, 0)
    delta  = timedelta(days=35)
    end_date = start + delta
    end = datetime(end_date.year, end_date.month, 1, 0)
    month_str = get_month_name(start.month)
    title = f"Pörssisähkön keskihinnat {month_str}ssa {start.year}"
    data_item = Timespan(start, end, title)
    data_item.init_data_item()

    return data_item



