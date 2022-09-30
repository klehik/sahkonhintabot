from datetime import timedelta, datetime


from DataItem import Day, Timespan

from utils import get_month_name

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







