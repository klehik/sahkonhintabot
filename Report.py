from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from matplotlib.text import OffsetFrom
import pandas as pd
from entsoe import  EntsoePandasClient
from utils import get_ranges, format_price
from PIL import Image
import logging
import numpy as np
from graph_utils import add_bar_labels, legend_position
import warnings
warnings.filterwarnings("ignore")
plt.set_loglevel(level="error")

class Report:
    def __init__(self, start, end, title) -> None:
        self.dataframe = None
        self.start = start
        self.end = end
        self.country = os.getenv("COUNTRY")
        self.tz = os.getenv("TIMEZONE")
        self.bar_graph_path = None
        self.timeframe_str = f"{self.start.day}-{self.start.month}-{self.start.year}-{self.end.day}-{self.end.month}-{self.end.year}"
        self.insights = None
        self.title = title

    def calculte_insights(self):
        df = self.dataframe

        mean = df['price'].mean()
        min = df['price'].min()
        max = df['price'].max()
       

        self.insights = {"mean": mean, "min": min, "max": max}
    

    def init_report(self):
        start = pd.Timestamp(self.start, tz=self.tz)
        end = pd.Timestamp(self.end, tz=self.tz)

        client = EntsoePandasClient(os.getenv("ENTSO_API_KEY"))
        data = client.query_day_ahead_prices(self.country, start=start,end=end)
        df = data.to_frame()
        df = df[:-1]
        df.rename(columns = {0: "price_€/MWh"}, inplace = True)
        df['date'] = df.index
        df['date_str'] = df['date'].astype(str)
        df['month'] = df.index.month
        df['day'] = df.index.day
        df['year'] = df.index.year
        df['hour'] = df.index.hour
        df['price_tax_0'] = round(df['price_€/MWh']/10, 2)
        df['price_tax_24'] = round(df['price_€/MWh']*1.24 / 10, 2)
        df['price_tax_10'] = round(df['price_€/MWh']*1.1 / 10, 2)
        df['price'] = df['price_tax_0']
        self.dataframe = df
        self.calculte_insights()

    def plot_bar_graph(self, settings):
        logging.info("Plotting bar graph")
        df = self.dataframe

                

        x = df['date_str']
        y = df['price']

        plt.rc("font", size=18)          # controls default text sizes
        
        plt.rc("axes", labelsize=14)    # fontsize of the x and y labels
        plt.rc("xtick", labelsize=14)    # fontsize of the tick labels
        plt.rc("ytick", labelsize=14)    # fontsize of the tick labels
     
        fig, ax = plt.subplots()
        ax.set_xticklabels(df['hour'])
        
        fig.set_size_inches(12,6)

        max = df['price'].max()
        mean = df['price'].mean()
        min = df['price'].min()
       
        # bar chart
        col = []
        for val in y:
            if val < 10:
                col.append('green')
            elif val <= 20:
                col.append('orange')
            else:
                col.append('red')


        plt.bar(x, y, color = col)
        if settings['bar_labels']:
            add_bar_labels(x, y, max, 7)

        title = f"Pörssisähkön tuntihinnat {self.timeframe_str} (alv 0%)"

        plt.title(title)
        plt.xlabel("Tunti")
        plt.ylabel("Hinta snt/kWh")
        plt.figtext(0.90, 0.04, "Lähde: ENTSO-E", fontsize=9)

        

        if min < 0:
            plt.ylim(bottom=min-(max/25 + 0.2))
            plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        if max < 5:
            plt.ylim(top=max*2)
            

        filename = f'{self.timeframe_str}.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        im1 = Image.open(path)
        im2 = Image.open('./resources/legend_sb3.png')

        

        
        legend_x, legend_y = legend_position(y, max, settings['bars_from_start'])



        im1.paste(im2, (legend_x, legend_y))
        im1.save(path)

        self.bar_graph_path = path

class DayReport(Report):
    def __init__(self, start, end, title):
        super().__init__(start, end, title)
        self.date = f"{self.start.day}.{self.start.month}.{self.start.year}"
        self.timeframe_str = f"{self.start.day}.{self.start.month}.{self.start.year}"
        self.avg_7_day = self.get_7_avg()
        self.avg_28_day = self.get_28_avg()
    

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



    def get_7_avg(self):
        
        one_week = timedelta(days=7)
        title = f"Pörssisähkön 7 vrk:n tuntihinnat"
        report = TimespanReport(start=self.end-one_week, end=self.end, title=title)
        report.init_report()

        return report


    def get_28_avg(self):
        
        one_month = timedelta(days=28)
        title = f"Pörssisähkön päiväkohtaiset keskihinnat"
        report = TimespanReport(start=self.end-one_month, end=self.end, title=title)
        report.init_report()

        return report

class TimespanReport(Report):
    def __init__(self, start, end, title):
        super().__init__(start, end, title)
        self.title = title
        

    

    def plot_bar_graph(self, settings):
        logging.info("Plotting bar graph")
        df = self.dataframe

        df2 = pd.DataFrame()


        df2['average_price'] = df.groupby('day')['price_€/MWh'].mean()
        df2['month'] = df.groupby('day')['month'].max()
        df2['average_price'] = round(df2['average_price']/10, 2)


        df2.sort_values(['month', 'day'], inplace=True)
        df2.reset_index(inplace=True)
        df2['xtick_label'] = df2['day'].astype(str) + "." + df2['month'].astype(str)

        if settings['hourly']:
            x = df['date_str']
            y = df['price']  
            plt.xlabel("Tunti")
            
        else:
            x = df2['xtick_label'].tolist()
            y = df2['average_price']
            plt.xlabel("Päivä")

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
        plt.bar(x, y, color = col)
        if not settings['hourly']:
            add_bar_labels(x, y, max, settings['bar_label_font_size'])



        fig.set_size_inches(12,6)
        title = f"{self.title} (alv 0%)"
        plt.title(title)
        plt.figtext(0.90, 0.05, "Lähde: ENTSO-E", fontsize=9)
        if settings['hourly']:
            plt.xticks(np.arange(-0.5, len(x), 24))
        
        plt.ylabel("Hinta snt/kWh")
        

        filename = f'{self.timeframe_str}.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        im1 = Image.open(path)
        im2 = Image.open('./resources/legend_sb3.png')

      

        max = y.max()

        legend_x, legend_y = legend_position(y, max, settings['bars_from_start'])

        im1.paste(im2, (legend_x, legend_y))
        im1.save(path)

        self.bar_graph_path = path

        