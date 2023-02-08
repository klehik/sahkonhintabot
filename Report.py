from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import decimal
import pandas as pd
from entsoe import  EntsoePandasClient
from utils import get_ranges, format_price, round_half_up
from PIL import Image
import logging
import numpy as np
from graph_utils import add_bar_labels, legend_position, preprocess_dataframe
import warnings
warnings.filterwarnings("ignore")
plt.set_loglevel(level="error")

class Report:
    def __init__(self, start, end, title) -> None:
        self.dataframe = None
        self.start = start
        self.end = end
        self.tax = os.getenv("TAX")
        self.country = os.getenv("COUNTRY")
        self.tz = os.getenv("TIMEZONE")
        self.bar_graph_path = None
        self.timeframe_str = f"{self.start.day}-{self.start.month}-{self.start.year}-{self.end.day}-{self.end.month}-{self.end.year}"
        self.insights = None
        self.title = title + f' (alv {self.tax}%)'

    def calculate_insights(self):
        df = self.dataframe
        mean = df['price'].mean()
        mean = round_half_up(mean, decimals=2)
        min = df['price_rounded'].min()
        max = df['price_rounded'].max()
        self.insights = {"mean": mean, "min": min, "max": max}
    

    def init_report(self):
        # get data and preprocess dataframe
        start = pd.Timestamp(self.start, tz=self.tz)
        end = pd.Timestamp(self.end, tz=self.tz)
        client = EntsoePandasClient(os.getenv("ENTSO_API_KEY"))
        data = client.query_day_ahead_prices(self.country, start=start,end=end)
        
        df = data.to_frame()
        self.dataframe = preprocess_dataframe(df, self.tax)
        self.calculate_insights()



class DayAheadReport(Report):
    def __init__(self, start, end, title):
        super().__init__(start, end, title)
        self.date = f"{self.start.day}.{self.start.month}.{self.start.year}"
        self.timeframe_str = self.date

    def calculate_below_average_periods(self):
        
        df = self.dataframe
        df.index = df['hour']
        df3 = df[df['price'] < df['price'].mean()]

        ranges = get_ranges(df3.index)
            
        periods = []
        for r in ranges:
            start = r[0]
            end = r[1]
            
            prices = [df.iloc[i].price for i in range(start, end+1)]
            mean = sum(prices)/len(prices)
            periods.append((start, end+1, round(mean, 2)))
    

        return periods

    def plot_bar_graph(self, settings):
        logging.info("Plotting bar graph")
        df = self.dataframe

        x = df['date_str']
        y = df['price_rounded']

        plt.rc("font", size=18) # controls default text sizes
        plt.rc("axes", labelsize=14) # fontsize of the x and y labels
        plt.rc("xtick", labelsize=14) # fontsize of the tick labels
        plt.rc("ytick", labelsize=14) # fontsize of the tick labels
     
        fig, ax = plt.subplots()
        fig.set_size_inches(12,6)
        ax.set_xticklabels(df['hour'])

        max = self.insights['max']
        mean = self.insights['mean']
        min = self.insights['min']

        # bar colors
        col = []
        for val in y:
            if val < 10:
                col.append('green')
            elif val <= 20:
                col.append('orange')
            else:
                col.append('red')

        plt.bar(x, y, color = col)
        
        # labels 
        if settings['bar_labels']:   
            add_bar_labels(x, y, max, 7)

        plt.title(self.title)
        plt.xlabel("Tunti")
        plt.ylabel("Hinta snt/kWh")
        plt.figtext(0.90, 0.04, "Lähde: ENTSO-E", fontsize=9)

        
        # add ylim and 0-line if negative prices
        if min < 0:
            plt.ylim(bottom=min-(max/25 + 0.2))
            plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # add ylim 
        """ if max < 5:
            plt.ylim(top=max*2)
            max = max*2 """
        if max < 20:
            plt.ylim(top=20)
            max = 20
            
        # save locally
        filename = f'{self.date}.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        # adding legend
        im1 = Image.open(path)
        im2 = Image.open('./resources/legend_sb3.png')
        # calculate legend position
        legend_x, legend_y = legend_position(y, max, settings['bars_from_start'])
        im1.paste(im2, (legend_x, legend_y))
        im1.save(path)

        self.bar_graph_path = path


class TimespanReport(Report):
    def __init__(self, start, end, title):
        super().__init__(start, end, title)
        
        
    def plot_bar_graph(self, settings):
        logging.info("Plotting bar graph")
        df = self.dataframe
        
        # another dataframe for daily averages
        df2 = pd.DataFrame()
        df2['average_price'] = df.groupby('day')['price'].mean()
        df2['month'] = df.groupby('day')['month'].max()
        df2['year'] = df.groupby('day')['year'].max()
        # rounding
        df2['average_price'] = (df2['average_price']).map(lambda x: round_half_up(x, decimals=2))

        df2.sort_values(['year', 'month', 'day'], inplace=True)
        df2.reset_index(inplace=True)
        df2['xtick_label'] = df2['day'].astype(str) + "." + df2['month'].astype(str)
        

        if settings['hourly']:
            x = df['date_str']
            y = df['price_rounded']  
            plt.xlabel("Tunti")
            
        else:
            x = df2['xtick_label'].tolist()
            y = df2['average_price']
            plt.xlabel("Päivä")
        plt.ylabel("Hinta snt/kWh")

        plt.rc("font", size=18)          # controls default text sizes 
        plt.rc("axes", labelsize=14)    # fontsize of the x and y labels
        plt.rc("xtick", labelsize=14)    # fontsize of the tick labels
        plt.rc("ytick", labelsize=14)    # fontsize of the tick labels
        
        fig, ax = plt.subplots()
     
        ax.set_xticklabels(df2['xtick_label'].tolist())
        plt.xticks(rotation = settings['label_rotation'])

        col = []
        for val in y:
            if val < 10:
                col.append('green')
            elif val <= 20:
                col.append('orange')
            else:
                col.append('red')

        max = y.max()
        min = y.min()

        plt.bar(x, y, color = col)
        if not settings['hourly']:
            add_bar_labels(x, y, max, settings['bar_label_font_size'])

        # add ylim if prices are very low and horizontal 0-line if prices are negative
        if min < 0:
            plt.ylim(bottom=min-(max/25 + 0.2))
            plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        if max < 20:
            plt.ylim(top=20)
            max = 20

        fig.set_size_inches(12,6)
        plt.title(self.title)
        plt.figtext(0.90, 0.05, "Lähde: ENTSO-E", fontsize=9)

        if settings['hourly']:
            plt.xticks(np.arange(-0.5, len(x), 24))
        
        filename = f'{self.timeframe_str}.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        # adding legend
        im1 = Image.open(path)
        im2 = Image.open('./resources/legend_sb3.png')
        # calculate legend position
        legend_x, legend_y = legend_position(y, max, settings['bars_from_start'])
        im1.paste(im2, (legend_x, legend_y))

        im1.save(path)
        self.bar_graph_path = path

        


