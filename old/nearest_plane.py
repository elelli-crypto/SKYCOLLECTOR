import requests
import math

# 내 위치: 일단 인천공항 기준
my_lat = 37.4602
my_lon = 126.4407

url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()
states = data["states"]


def calculate_distance(lat1, lon1, lat2, lon2):
    # 위도/경도 차이를 이용해서 대략적인 거리(km)를 계산
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2

    distance = math.sqrt(lat_diff ** 2 + lon_diff ** 2) * 111
    return distance


nearest_plane = None
nearest_distance = 999999

for plane in states:
    callsign = plane[1]
    country = plane[2]
    longitude = plane[5]
    latitude = plane[6]
    altitude = plane[7]
    velocity = plane[9]

    if longitude is not None and latitude is not None:
        if 120 <= longitude <= 140 and 30 <= latitude <= 45:

            if altitude is not None and altitude > 1000:

             distance = calculate_distance(my_lat, my_lon, latitude, longitude)

             if distance < nearest_distance:
                     nearest_distance = distance
                     nearest_plane = {
                     "callsign": callsign,
                     "country": country,
                      "latitude": latitude,
                     "longitude": longitude,
                        "altitude": altitude,
                        "velocity": velocity
                 }

print("가장 가까운 비행기")
print("-------------------")
print("비행기:", nearest_plane["callsign"])
print("국가:", nearest_plane["country"])
print("거리:", round(nearest_distance, 2), "km")
print("고도:", nearest_plane["altitude"], "m")
print("속도:", nearest_plane["velocity"], "m/s")