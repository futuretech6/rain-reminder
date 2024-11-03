import json
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import DefaultDict, List

import requests
import toml

config = toml.load("config.toml")
locations = config["location"]
api_key = os.environ["APIKEY"]

# {location, {condition, [time]}}
location_results: DefaultDict[
    str, DefaultDict[str, List[datetime]]
] = defaultdict(lambda: defaultdict(list))

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
                api_key,
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
        if (condition := forecast["weather"][0]["main"]) in {
            "Thunderstorm",
            "Drizzle",
            "Rain",
            "Snow",
        }:  # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
            location_results[location][condition].append(forecast_time)

if len(location_results) != 0:
    for location, conditions in location_results.items():
        print(f"{location} will be ", end="")
        for condition, dt_list in conditions.items():
            print(f"{condition.lower()} at ", end="")
            print(
                ", ".join(
                    ["{}:{:02}".format(dt.hour, dt.minute) for dt in dt_list]
                ),
                end="; ",
            )
        print()
    exit(2)  # exit to make actions alarm
else:
    print("sunny everywhere, happy!")
