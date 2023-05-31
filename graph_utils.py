import matplotlib.pyplot as plt
import logging
from utils import format_price, round_half_up
from datetime import datetime


def add_bar_labels(x, y, max, fontsize):
    # calculate relative bar label distance
    for i in range(len(x)):

        offset = max / 90

        if y[i] < 0:
            offset = offset * -1
            plt.text(
                i,
                y[i] + offset,
                format_price(y[i]),
                fontdict={"fontsize": fontsize, "weight": "bold"},
                ha="center",
                va="top",
            )

        else:
            plt.text(
                i,
                y[i] + offset,
                format_price(y[i]),
                fontdict={"fontsize": fontsize, "weight": "bold"},
                ha="center",
            )


def legend_position(y, max, bars_from_start_or_end):
    legend_is_on_first_bars = False
    legend_is_on_last_bars = False
    treshold = max * 0.70
    logging.debug("Legend treshold: {}".format(treshold))
    for val in y[0:bars_from_start_or_end]:
        if val > treshold:
            legend_is_on_first_bars = True

    for val in y[-bars_from_start_or_end:]:
        if val > treshold:
            legend_is_on_last_bars = True

    if legend_is_on_first_bars and legend_is_on_last_bars:
        return 1085, 90
    elif legend_is_on_first_bars:
        return 950, 90
    else:
        return 170, 90


def add_tax_convert_ckwh(val, tax):

    tax_formatted = int(tax) / 100 + 1

    if val < 0:
        return round_half_up(val / 10, decimals=3)
    else:
        return round_half_up((val * tax_formatted) / 10, decimals=3)


def add_tax_convert_ckwh_row(row, tax):
    # calculating tax for months that has temporary tax change
    new_row = []
    tax_formatted = int(tax) / 100 + 1
    for indx, val in row.items():

        if indx.month <= 4:
            if val < 0:
                new_row.append(round_half_up(val / 10, decimals=3))
            else:
                new_row.append(round_half_up((val * 1.1) / 10, decimals=3))
        else:

            if val < 0:
                new_row.append(round_half_up(val / 10, decimals=3))
            else:
                new_row.append(round_half_up((val * tax_formatted) / 10, decimals=3))

    return new_row


def preprocess_dataframe(df, tax):

    df = df[:-1]
    df.rename(columns={0: "price_€/MWh"}, inplace=True)
    df["date"] = df.index
    df["date_str"] = df["date"].astype(str)
    df["month"] = df.index.month
    df["day"] = df.index.day
    df["year"] = df.index.year
    df["hour"] = df.index.hour

    # df["price"] = add_tax_convert_ckwh_row(df["price_€/MWh"], tax)
    df['price'] = (df['price_€/MWh']).map(lambda x: add_tax_convert_ckwh(x, tax))
    df["price_rounded"] = df["price"].map(lambda x: round_half_up(x, decimals=2))

    return df

