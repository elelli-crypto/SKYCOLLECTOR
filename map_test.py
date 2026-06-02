import requests
import folium
import webbrowser
import os
import math

my_lat = 37.4602
my_lon = 126.4407

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

count = 0

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
            count += 1

            popup_text = f"""
                <h3>✈️ {callsign}</h3>

                <b>출발 국가:</b> {country}<br>

                <b>현재 고도:</b> {altitude} m<br>

                <b>현재 속도:</b> {velocity} m/s<br><br>

                🌍 지금 이 비행기는 당신 위의 하늘을 지나가는 중입니다.
                """
            distance = calculate_distance(my_lat, my_lon, latitude, longitude)

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
print("한국 근처 비행기 수:", count)

file_name = "sky_map_nearest.html"
m.save(file_name)

webbrowser.open("file://" + os.path.realpath(file_name))