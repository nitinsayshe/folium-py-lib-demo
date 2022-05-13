#  install the folium lib
import folium
import pandas as pd

import numpy as np
from geopy.geocoders import ArcGIS   #convert the adress to long and lati
arc=ArcGIS()

df=pd.read_csv("house_price_data.csv")
df.dropna(inplace=True)

df["Address"]=df["street"]+","+df["city"]+","+df["statezip"]+","+df["country"]

df["Coordinate"]=df["Address"].apply(arc.geocode) #convert the adress to long and lati

lati=df["Coordinate"].map(lambda x:x.latitude)
long=df["Coordinate"].map(lambda x:x.longitude)


latitude=list(lati)
longitude=list(long)

price=list(df["price"]) #int
cnd=list(df["condition"])

def color_code(condition):
    if condition<2:
        return "red"
    elif 2<condition<4:
        return "orange"
    elif condition>=4:
        return "green"

map=folium.Map(location=[latitude[0],longitude[0]],zoom_start=9) #tiles="Stamen Terrain" base layer

fg=folium.FeatureGroup(name="My Map")

for i,j,k,c in zip(latitude,longitude,price,cnd):
    fg.add_child(folium.CircleMarker(location=[i,j],radius=10,popup="price:"+str(k)+" rs",
                                     fill_color=color_code(c)))

map.add_child(fg)

map.save("Out_map.html")

