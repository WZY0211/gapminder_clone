import pandas as pd
import sqlite3 
import plotly.express as px


connection = sqlite3.connect("data/gapminder.db")
plotting_of =  pd.read_sql("""SELECT * FROM plotting;""", con=connection)
connection.close()

fig = px.scatter(plotting_of, 
                 x="gdp_per_capita", y="life_expectancy", 
                 animation_frame="dt_year", # 每一個動畫幀的時間單位是年份
                 animation_group="country_name", # 每個泡泡代表一個國家
                 size="population", color="continent", 
                 hover_name="country_name",  # 滑鼠移到泡泡上時顯示的國家名稱
                 size_max=100, # 最大泡泡大小
                 range_x=[500, 100000], range_y=[20, 90], 
                 log_x=True, # X 軸使用對數刻度（讓資料分布更清楚）
                 title="Gapminder Clone 1800-2023")
fig.write_html("gapminder_clone.html", auto_open=True)