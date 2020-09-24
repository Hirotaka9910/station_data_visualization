#%%
import pandas as pd
import folium
from folium.plugins import HeatMap

#ファイル読み込み
station = pd.read_csv(r"station_data_visualization/station_geocode.csv")
station_data = pd.read_excel(r"station_data_visualization/東京近郊駅データ.xlsx",sheet_name="駅周辺地域データ")
#station.loc[:,["id","lat","lon"]]



#%%　station_dataに座標を結合
station_data_2 = pd.merge(station_data,station.loc[:,["id","lat","lon"]], how = "inner", on = "id")
#station_data_2

#%%　ここからmap作成

#mapの生成
map = folium.Map(location=[35.6908333333333, 139.700277777778], zoom_start=10)

#heatmap作成用の変数
import math

coordinate = list()

###　データが入っていないものについては値0として処理
for i in range(len(station_data_2)):
    if math.isnan(station_data_2["乗降客数(日)"][i]) == False:
        data = (station_data_2['lat'][i],station_data_2['lon'][i],station_data_2["乗降客数(日)"][i]/10000)
        coordinate.append(data)
    else:
        data = (station_data_2['lat'][i],station_data_2['lon'][i],0)
        coordinate.append(data)
#coordinate

#%% 整形したデータをマップに付加して保存
HeatMap(coordinate, radius=20).add_to(map)
map.save('heatmap_乗降客数.html')
