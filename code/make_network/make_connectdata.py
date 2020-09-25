"""
スクレイピングで取得済みの愛知県を通る路線の通過駅駅リストがある（station_data_aichi.csv）
このデータから駅の接続データを作成する（ネットワーク化には接続情報が必要なため）
"""

#%%
import pandas as pd

#%%  駅リストはline_idが同じであれば前後は接続する順位並んでいる
data = pd.read_csv(r"station_data_visualization/data/station_data_aichi.csv")
data

#%%
line = pd.read_csv(r"station_data_visualization/data/rail_data_aichi.csv")
line

#%% 格納用のデータフレーム作成
connect_data = pd.DataFrame(columns = ["company_id","line_id","from_station_id","to_station_id","from_lat","from_lon","to_lat","to_lon"])



#%%
count = 0
for i in range(len(line)):
    #それぞれの路線の通過駅を抽出
    company_id = data["company_id"][i]
    line_id = line["line_id"][i]
    path = data[data["line_id"] == line_id]
    path = path.reset_index()
    for j in range(len(path)-1):
        from_station_id = path["station_id"][j]
        from_station = path["station_name"][j]
        from_lat = path["lat"][j]
        from_lon = path["lon"][j]

        to_station_id = path["station_id"][j+1]
        to_station = path["station_name"][j+1]
        to_lat = path["lat"][j+1]
        to_lon = path["lon"][j+1]

        connect_list = [company_id,line_id,from_station_id,to_station_id,from_lat,from_lon,to_lat,to_lon]
        connect_data.loc[count] = connect_list
        count += 1

#なぜかid関連がfloatになるのでintにキャスト
connect_data['company_id'] = connect_data['company_id'].astype('int')
connect_data['line_id'] = connect_data['line_id'].astype('int')
connect_data['from_station_id'] = connect_data['from_station_id'].astype('int')
connect_data['to_station_id'] = connect_data['to_station_id'].astype('int')

connect_data

#csvで保存
connect_data.to_csv(r"station_data_visualization/data/master_aichi.csv",index=False)
