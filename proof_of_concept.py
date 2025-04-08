import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#從plotting檢視表選取所有資料
connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting;""", con=connection)
connection.close()

#透過matplotlib繪圖
fig, ax = plt.subplots()
def update_plot(year_to_plot: int):
    ax.clear() # 每次都要清空前一年份的軸物件
    subset_df = plotting_df[plotting_df["dt_year"] == year_to_plot]   # 靜態圖可先定義 year_to_plot = 年份
    lex = subset_df["life_expectancy"].values # y軸 壽命
    gdp_pcap = subset_df["gdp_per_capita"].values # x軸 各國人均DDP
    cont = subset_df["continent"].values # 洲別
    color_map = {
        "asia":"r",
        "africa":"g",
        "europe":"b",
        "americas":"c" #cyan
    }

    for xi, yi, ci in zip(gdp_pcap, lex, cont):
        ax.scatter(xi, yi, color=color_map[ci]) # 根據 ci（洲別）查出對應的顏色 color_map[ci]
    ax.set_title(f"The world in {year_to_plot}")
    ax.set_xlabel("GDP Per Capita(in USD)")
    ax.set_ylabel("Life Expectancy")
    ax.set_xlim(0, 100000)
    ax.set_ylim(20, 100)
ani = animation.FuncAnimation(fig, func=update_plot, frames=range(2000,2024), interval=10)
ani.save("animation.gif", writer="pillow", fps=10)
