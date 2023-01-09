import json
from datetime import datetime

import requests

APP_ID = "---------------------"
API_KEY = "---------------------"
BASE_URL = "https://trackapi.nutritionix.com/"
EXERCISE_URL = "v2/natural/exercise"
SHEETY_POST_ENDPOINT = "---------------------"
SHEETY_TOKEN = "---------------------"

# _________ NUTRITIONIX API _________
nutritionix_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
user_exercise = input("What exercise did you complete today?\n")
nutritionix_params = {
    "query": user_exercise,
    "gender": "female",
    "weight_kg": 68,
    "height_cm": 175,
    "age": 30
}
response = requests.post(url=f"{BASE_URL}{EXERCISE_URL}",
                         json=nutritionix_params,
                         headers=nutritionix_header)
response.raise_for_status()
data = response.json()
with open("temp_data.json", mode="w") as file:
    json.dump(data, file)

for exercise in data["exercises"]:
    today = datetime.now()
    date = today.strftime("%x")
    time = today.strftime("%X")
    activity = exercise["name"].title()
    duration = exercise["duration_min"]
    calories = exercise["nf_calories"]

    # _________ SHEETY API _________
    # a better way to do this is to just combine below dict into the above var decl but i feel like this is easier to read.
    sheety_json = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": activity,
            "duration": duration,
            "calories": calories,
        }
    }
    # upload workout data to sheety
    header = {"Authorization": SHEETY_TOKEN}
    response = requests.post(url=f"{SHEETY_POST_ENDPOINT}",
                             json=sheety_json,
                             headers=header)
    data = response.json()
    print(data)
    if "errors" not in data:
        print(f"uploaded {activity} data successfully")
