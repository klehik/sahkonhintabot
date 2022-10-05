from datetime import timedelta, datetime


from Report import DayReport, TimespanReport

from utils import get_month_name

def generate_day_report(date: datetime):
    
    start = datetime(date.year, date.month, date.day, 0)
    one_day = timedelta(days=1)
    title = f""
    report = DayReport(start=start, end=start+one_day, title=title)
    report.init_report()

    return report

def generate_week_report(date):
    # +1 days = today
    date = datetime(date.year, date.month, date.day)
    end = date + timedelta(days=1)
    start = end - timedelta(days=7)
    title = f"Pörssisähkön 7 vrk:n tuntihinnat"
    report = TimespanReport(start=start, end=end, title=title)
    report.init_report()

    return report


def generate_month_report(date):

    start = datetime(date.year, date.month, 1, 0)
    delta  = timedelta(days=35)
    end_date = start + delta
    end = datetime(end_date.year, end_date.month, 1, 0)
    month_str = get_month_name(start.month)
    title = f"Pörssisähkön keskihinnat {month_str}ssa {start.year}"
    report = TimespanReport(start, end, title)
    report.init_report()

    return report







