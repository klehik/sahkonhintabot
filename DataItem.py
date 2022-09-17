from datetime import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
from entsoe import  EntsoePandasClient
from utils import format_price, get_ranges
from PIL import Image

class DataItem:
    def __init__(self, start, end, country, timezone) -> None:
        # dataframe
        #                  date_str      0    month day hour  price
        # 2022-09-15 00:00:00+03:00  34.16        9  15    0   3.42

        self.dataframe = None
        self.start = start
        self.end = end
        self.country = country
        self.tz = timezone
        self.bar_graph_path = None
        self.date = f"{self.start.day}.{self.start.month}.{self.start.year}"

    def calculte_insights(self):
        df = self.dataframe

        mean = df['price'].mean()
        mean = format_price(mean)

        min = df['price'].min()
        min = format_price(min)

        max = df['price'].max()
        max = format_price(max)

        return {"mean": mean, "min": min, "max": max}

    def calculate_below_average_hours(self):
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
        

    def get_market_price_dataframe(self):
        start = pd.Timestamp(self.start, tz=self.tz)
        end = pd.Timestamp(self.end, tz=self.tz)

        client = EntsoePandasClient(os.getenv("ENTSO_API_KEY"))
        data = client.query_day_ahead_prices(self.country, start=start,end=end)
        df = data.to_frame()
        df = df[:-1]
        df['date'] = df.index
        df['date_str'] = df['date'].astype(str)
        df['month'] = df.index.month
        df['day'] = df.index.day
        df['hour'] = df.index.hour
        df['price'] = round(df[0]/10, 2) 
        print(df)
        self.dataframe = df
        

    def plot_bar_graph(self):
        df = self.dataframe

        def add_bar_labels(x,y):
            for i in range(len(x)):
                plt.text(i, y[i] + 0.2, y[i], fontdict={"fontsize": 8, "weight": "bold"}, ha = "center")

        x = df['date_str']
        y = df['price']

        plt.rc("font", size=18)          # controls default text sizes
        
        plt.rc("axes", labelsize=14)    # fontsize of the x and y labels
        plt.rc("xtick", labelsize=14)    # fontsize of the tick labels
        plt.rc("ytick", labelsize=14)    # fontsize of the tick labels
       
        fig, ax = plt.subplots()
        ax.set_xticklabels(df['hour'])
        fig.set_size_inches(12,6)
       
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
        
        add_bar_labels(x, y)

        # title_long = f"Pörssisähkön hinta {self.date} {df['hour'][0]}:00 - {df['day'][-1]}/{df['month'][-1]} {df['hour'][-1] +1}:00 (alv 0%)" 
        title_short = f"Pörssisähkön hinta {self.date} (alv 0%)" 

        plt.title(title_short)
        plt.xlabel("Tunti")
        plt.ylabel("Hinta snt/kWh")
        

        filename = 'bar.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        im1 = Image.open(path)
        im2 = Image.open('./images/legend_sb3.png')

        legend_is_on_bars = False

        max = df['price'].max()
        treshold = max * 0.70
        print('legend_treshold', treshold)
        for val in y[0:5]:
            if val > treshold:
                legend_is_on_bars = True

        if legend_is_on_bars:
            legend_x = 8
            legend_y = 12
        else:
            legend_x = 170
            legend_y = 90

        im1.paste(im2, (legend_x, legend_y))
        im1.save(path)

        self.bar_graph_path = path