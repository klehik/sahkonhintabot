from datetime import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
from entsoe import  EntsoePandasClient
from utils import format_price

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

    def generate_insights(self):
        df = self.dataframe

        mean = df['price'].mean()
        mean = format_price(mean)

        min = df['price'].min()
        min = format_price(min)

        max = df['price'].max()
        max = format_price(max)

        return {'mean': mean, 'min': min, 'max': max}
        

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
                plt.text(i, y[i] + 0.2, y[i], fontdict={'fontsize': 8, 'weight': 'bold'}, ha = 'center')

        x = df['date_str']
        y = df['price']

        SMALL_SIZE = 10
        MEDIUM_SIZE = 14
        LARGE_SIZE = 18

        plt.rc('font', size=LARGE_SIZE)          # controls default text sizes
        #plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels


        fig, ax = plt.subplots()
        ax.set_xticklabels(df['hour'])
        fig.set_size_inches(12,6)

        # bar chart
        plt.bar(x, y, width=0.8)
        add_bar_labels(x, y)

        title_long = f"Pörssisähkön hinta {self.date} {df['hour'][0]}:00 - {df['day'][-1]}/{df['month'][-1]} {df['hour'][-1] +1}:00 (alv 0%)" 
        title_short = f"Pörssisähkön hinta {self.date} (alv 0%)" 

        plt.title(title_short)
        plt.xlabel("Tunti")
        plt.ylabel("snt/kWh")

        filename = 'bar.png'
        path = f"./images/{filename}"
        plt.savefig(path)

        self.bar_graph_path = path