import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List

import requests
import toml

config = toml.load("config.toml")
locations = config["location"]
apikey = os.environ["APIKEY"]

location_results: Dict[str, List[datetime]] = {}

for location in locations:
    longitude = locations[location]["longitude"]
    latitude = locations[location]["latitude"]
    local_time = datetime.utcnow() + timedelta(hours=longitude // 15)
    tomorrow = local_time.date() + timedelta(days=1)
    while True:
        response = requests.get(
            url="http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(
                latitude,
                longitude,
                apikey,
            )
        )
        if (
            response.status_code == 200
            and (info := json.loads(response.text))["cod"] == "200"
        ):
            break
        else:
            time.sleep(10)

    for forecast in info["list"]:
        forecast_time = datetime.fromtimestamp(forecast["dt"])
        if forecast_time.date() != tomorrow:
            continue
        if forecast["weather"][0]["main"] == "Rain":
            if location not in location_results:
                location_results[location] = []
            location_results[location].append(forecast_time)

if len(location_results) != 0:
    for location in location_results:
        print("{} will be rainy at ".format(location), end="")
        time_str: str = ""
        for dt in location_results[location]:
            time_str += "{}:{:02}, ".format(dt.hour, dt.minute)
        print(time_str.rstrip(", "))
    exit(2)  # exit to make actions alarm
else:
    print("sunny everywhere, happy!")
