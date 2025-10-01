from datetime import datetime
import calendar
import decimal
from decimal import Decimal, ROUND_HALF_UP
import os

def format_price(value):

    price = format(value, ".2f")
    price = str(price).replace('.', ',')
    return price


def convert_to_ckwh(value):
    value = round(value / 10, 2)
    if value == -0:

        value = 0.0
    return value


def round_half_up(val, decimals):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    val = Decimal(str(val))

    val = round(val, decimals)
    val = float(val)
    if val == -0.00:
        val = 0.00
    return val


def get_ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s + 1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


def get_month_name(month):
    switch = {
        1: "tammikuu",
        2: "helmikuu",
        3: "maaliskuu",
        4: "huhtikuu",
        5: "toukokuu",
        6: "kesäkuu",
        7: "heinäkuu",
        8: "elokuu",
        9: "syyskuu",
        10: "lokakuu",
        11: "marraskuu",
        12: "joulukuu",
    }
    return switch.get(month, "")


def get_days_in_month(date: datetime):
    monthrange = calendar.monthrange(date.year, date.month)
    return monthrange[1]


def format_difference(value):
    if value > 0:
        return "+" + str(format_price(value))
    else:
        return str(format_price(value))


def format_percentage(value):
    value = round(value, 1)
    prefix = ""

    if value > 0:
        prefix = "+"

    value = format(value, ".1f")

    value = str(value).replace('.', ',')

    return prefix + value


def remove_file(file_path: str):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")
    else:
        print(f"File does not exist: {file_path}")


def get_missing_data():
    import pandas as pd

    ## missing data from May 28
    st = {
        pd.Timestamp(
            '2023-05-28 01:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -3.42,
        pd.Timestamp(
            '2023-05-28 02:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -3.56,
        pd.Timestamp(
            '2023-05-28 03:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -4.12,
        pd.Timestamp(
            '2023-05-28 04:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -3.88,
        pd.Timestamp(
            '2023-05-28 05:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -4.48,
        pd.Timestamp(
            '2023-05-28 06:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -5.01,
        pd.Timestamp(
            '2023-05-28 07:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -4.38,
        pd.Timestamp(
            '2023-05-28 08:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -2.09,
        pd.Timestamp(
            '2023-05-28 09:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -1.04,
        pd.Timestamp(
            '2023-05-28 10:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -0.11,
        pd.Timestamp(
            '2023-05-28 11:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -3.08,
        pd.Timestamp(
            '2023-05-28 12:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -10.06,
        pd.Timestamp(
            '2023-05-28 13:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -10.03,
        pd.Timestamp(
            '2023-05-28 14:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -9.91,
        pd.Timestamp(
            '2023-05-28 15:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -10.00,
        pd.Timestamp(
            '2023-05-28 16:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -4.91,
        pd.Timestamp(
            '2023-05-28 17:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -5.04,
        pd.Timestamp(
            '2023-05-28 18:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): -0.06,
        pd.Timestamp(
            '2023-05-28 19:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 3.12,
        pd.Timestamp(
            '2023-05-28 20:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 2.00,
        pd.Timestamp(
            '2023-05-28 21:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 1.64,
        pd.Timestamp(
            '2023-05-28 22:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 1.53,
        pd.Timestamp(
            '2023-05-28 23:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 1.31,
        pd.Timestamp(
            '2023-05-29 00:00:00+0300', tz='Europe/Helsinki', freq='60T'
        ): 0.01,
    }
    return pd.Series(st)
