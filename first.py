import requests
import folium
import webbrowser
import os

url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()
states = data["states"]

# 서울 중심 지도
m = folium.Map(location=[37.5665, 126.9780], zoom_start=7)

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
        if 124 <= longitude <= 132 and 33 <= latitude <= 39:
            count += 1

            popup_text = f"""
            비행기: {callsign}<br>
            국가: {country}<br>
            고도: {altitude} m<br>
            속도: {velocity} m/s
            """

            folium.Marker(
                location=[latitude, longitude],
                popup=popup_text,
                tooltip=callsign
            ).add_to(m)

print("한국 근처 비행기 수:", count)

file_name = "sky_map.html"
m.save(file_name)

webbrowser.open("file://" + os.path.realpath(file_name))