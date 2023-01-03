from datetime import timedelta, datetime
from Report import TimespanReport, DayAheadReport
from utils import get_month_name
import logging


def generate_day_ahead_report(date: datetime):
    logging.info("Generating day ahead report")
    start = datetime(date.year, date.month, date.day, 0)
    days_1 = timedelta(days=1)
    title = f"Pörssisähkön tuntihinnat {date.day}.{date.month}.{date.year}"
    report = DayAheadReport(start=start, end=start+days_1, title=title)
    report.init_report()

    return report


def generate_7_day_report(date: datetime):
    logging.info("Generating 7-day report")
    end = datetime(date.year, date.month, date.day+1, 0)
    days_7 = timedelta(days=7)
    title = f"Pörssisähkön 7 vrk:n tuntihinnat"
    report = TimespanReport(start=end-days_7, end=end, title=title)
    report.init_report()

    return report

def generate_28_day_report(date: datetime):
    logging.info("Generating 28-day report")
    
    end = datetime(date.year, date.month, date.day+1, 0)
    days_28 = timedelta(days=28)
    title = f"Pörssisähkön päiväkohtaiset keskihinnat"
    report = TimespanReport(start=end-days_28, end=end, title=title)
    report.init_report()

    return report


def generate_month_report(date):
    logging.info("Generating monthly report")
    start = datetime(date.year, date.month, 1, 0)
    delta  = timedelta(days=35)
    end_date = start + delta
    end = datetime(end_date.year, end_date.month, 1, 0)
    month_str = get_month_name(start.month)
    title = f"Pörssisähkön keskihinnat {month_str}ssa {start.year}"
    report = TimespanReport(start, end, title)
    report.init_report()

    return report







