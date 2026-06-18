import requests
import folium
import webbrowser
import os
import math
from branca.element import Element

my_lat = 37.524838667326
my_lon = 126.924186745271

def calculate_distance(lat1, lon1, lat2, lon2):
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2

    distance = math.sqrt(lat_diff ** 2 + lon_diff ** 2) * 111
    return distance

url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()
states = data["states"]

# 서울 중심 지도
m = folium.Map(location=[37.5665, 126.9780], zoom_start=6)

folium.Marker(
    [my_lat, my_lon],
    popup="내 위치",
    icon=folium.Icon(color="green")
).add_to(m)

count = 0

min_distance = 999999

nearest_lat = None
nearest_lon = None
nearest_callsign = None
nearest_distance = None

collected_planes = set()

new_aircraft = ""

if os.path.exists("collector.txt"):
    with open("collector.txt", "r", encoding="utf-8") as f:
        for line in f:
            collected_planes.add(line.strip())

for plane in states:
    callsign = plane[1]
    country = plane[2]
    longitude = plane[5]
    latitude = plane[6]
    altitude = plane[7]
    velocity = plane[9]

    if longitude is not None and latitude is not None:
        # 한국 근처 범위
        if 120 <= longitude <= 140 and 30 <= latitude <= 45:
          

            distance = calculate_distance(
              my_lat,
              my_lon,
              latitude,
              longitude
            )

            if distance < min_distance:
              
              if callsign and callsign not in collected_planes:
                collected_planes.add(callsign)

                with open("collector.txt", "a", encoding="utf-8") as f:
                    f.write(callsign + "\n")

                new_aircraft = callsign

                print("새 비행기 발견!", callsign)

              min_distance = distance

              nearest_lat = latitude
              nearest_lon = longitude
              nearest_callsign = callsign
              nearest_distance = distance

            popup_text = f"""
                <h3>✈️ {callsign}</h3>

                <b>출발 국가:</b> {country}<br>

                <b>현재 고도:</b> {altitude} m<br>

                <b>현재 속도:</b> {velocity} m/s<br><br>

                🌍 지금 이 비행기는 당신 위의 하늘을 지나가는 중입니다.
                """
            distance = calculate_distance(my_lat, my_lon, latitude, longitude)
           
            if distance > 50:
                continue
            
            count += 1

            if distance < min_distance:
                min_distance = distance
                nearest_lat = latitude
                nearest_lon = longitude
                nearest_callsign = callsign
                nearest_distance = distance
            
            if distance < 20:
                marker_color = "red"
            else:
                marker_color = "blue"

            folium.Marker(
                    location=[latitude, longitude],
                    popup=popup_text,
                    tooltip="✈️ " + str(callsign),
                    icon=folium.Icon(color=marker_color, icon="plane", prefix="fa")
                ).add_to(m)
if nearest_lat is not None and nearest_lon is not None:
    folium.Marker(
        location=[my_lat, my_lon],
        popup="내 위치",
        tooltip="📍 내 위치",
        icon=folium.Icon(color="green", icon="user", prefix="fa")
    ).add_to(m)

    folium.PolyLine(
        locations=[
            [my_lat, my_lon],
            [nearest_lat, nearest_lon]
        ],
        color="red",
        weight=4,
        tooltip=f"가장 가까운 비행기: {nearest_callsign}"
    ).add_to(m)
print("50km 이내 비행기 수:", count)

file_name = "sky_map_nearest.html"

recent_planes = list(collected_planes)[-3:]
recent_text = "<br>".join(recent_planes)

info_box = f"""
<div style="
position: fixed;
top: 20px;
right: 20px;
width: 250px;
background-color: white;
border: 2px solid black;
padding: 10px;
z-index: 9999;
font-size: 14px;
">

<h4>✈ 가장 가까운 비행기</h4>

<b>콜사인:</b> {nearest_callsign}<br>
<b>거리:</b> {round(nearest_distance,2)} km<br>

<hr>
<b>수집한 비행기:</b> {len(collected_planes)} 대

<hr>
<b>최근 수집:</b><br>
{recent_text}

</div>
"""

if new_aircraft:

    popup_box = f"""
    <div style="
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 250px;
    background-color: gold;
    border: 3px solid black;
    padding: 15px;
    z-index: 9999;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    ">

    🎉 NEW AIRCRAFT<br><br>

    {new_aircraft}<br>
    발견!

    </div>
    """

    m.get_root().html.add_child(Element(popup_box))
m.get_root().html.add_child(Element(info_box))

m.save(file_name)

webbrowser.open("file://" + os.path.realpath(file_name))