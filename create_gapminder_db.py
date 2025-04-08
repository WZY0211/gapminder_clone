import pandas as pd
import sqlite3

class CreateGapminderDB:
    def __init__(self): #屬性
        self.file_names = ["ddf--datapoints--gdp_pcap--by--country--time",
             "ddf--datapoints--lex--by--country--time",
             "ddf--datapoints--pop--by--country--time",
             "ddf--entities--geo--country"]
        self.table_names = ["gdp_per_capita","life_expectancy","population","geography"]

    def import_as_dataframe(self):#方法
        # 建立一個空字典 df_dict，用來存放讀取的 CSV 資料
        df_dict = dict()
        for file_name, table_name in zip(self.file_names, self.table_names): # 使用 zip(file_names, table_names) 讓 file_names 和 table_names 兩個列表（list）配對
            file_path = f"data/{file_name}.csv" # f-string 格式化字串，將 file_name 插入字串，組合成 file_path
            df = pd.read_csv(file_path)
            df_dict[table_name] = df # 以 table_name 作為鍵，把 df 存入 df_dict 字典
        return df_dict

    def create_database(self):
        # 建立資料庫
        connection = sqlite3.connect("data/gapminder.db")
        df_dict = self.import_as_dataframe()
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")

        #建立檢視表
        drop_view_sql = """
        DROP VIEW IF EXISTS plotting;
        """
        create_view_sql = """
        CREATE VIEW plotting AS
        SELECT geography.name AS country_name,
               geography.world_4region AS continent,
               gdp_per_capita.time AS dt_year,
               gdp_per_capita.gdp_pcap AS gdp_per_capita,
               life_expectancy.lex AS life_expectancy,
               population.pop AS population
        FROM gdp_per_capita 
        JOIN geography ON gdp_per_capita.country = geography.country
        JOIN life_expectancy ON gdp_per_capita.country = life_expectancy.country AND gdp_per_capita.time = life_expectancy.time
        JOIN population ON gdp_per_capita.country = population.country AND gdp_per_capita.time = population.time
        WHERE gdp_per_capita.time < 2024;
        """
        cur = connection.cursor() #cursor（游標） 可以讓我們向 SQLite 資料庫發送查詢請求，例如 SELECT、INSERT、DELETE 等
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()

create_gapminder_db = CreateGapminderDB()
create_gapminder_db.create_database()