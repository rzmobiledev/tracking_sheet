import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
APPLICATION_ID = os.environ.get("APPLICATION_ID")
APPLICATION_KEY = os.environ.get("APPLICATION_KEY")

SHEETY_ENDPOINT = (
    "https://api.sheety.co/9bab5717a41a2ae826f78427ed68d66b/workoutTracking/email"
)
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")

HEADERS = {
    "x-app-id": APPLICATION_ID,
    "x-app-key": APPLICATION_KEY,
}

DATE = datetime.now()


def send_exercise_data(q: str, g: str, w_kg: float, h_cm: float, a: int):
    """
    Send all exercise datas and get all calories in return.
    param q is query:
    param g is gender:
    param w_kg is weight in kilograms:
    param h_cm is height in centi:
    param a is for age:
    """

    headers = HEADERS.copy()
    headers["Content-Type"] = "application/json"

    params = {
        "query": q.title(),
        "gender": g,
        "weight_kg": w_kg,
        "height_cm": h_cm,
        "age": a,
    }

    response = requests.post(url=API_ENDPOINT, json=params, headers=headers)
    response.raise_for_status()
    data = response.json()["exercises"]
    for exercise in data:
        save_workout(
            name=exercise["name"],
            duration_min=float(exercise["duration_min"]),
            calories=float(exercise["nf_calories"]),
        )
    return response.status_code


def save_workout(name: str, duration_min: float, calories: float):
    """
    Save workout information to google sheet
    """
    params = {
        "email": {
            "date": DATE.strftime("%Y/%m/%d"),
            "time": DATE.strftime("%H:%M:%S"),
            "exercise": name.title(),
            "duration": duration_min,
            "calories": calories,
        }
    }

    headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
    response = requests.post(
        url=SHEETY_ENDPOINT,
        json=params,
        headers=headers,
    )
    return response.status_code


def retrieve_exercise_informations():
    headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}

    response = requests.get(url=SHEETY_ENDPOINT, headers=headers)
    records = response.json()
    for record in records['email']:
        print(record)


# lets run the program
# send_exercise_data(
#     q=input("Tell me which exercise you did?: "), g="male", w_kg=80.2, h_cm=170, a=39
# )
# Ran 5K and cycled for 30 minutes.

retrieve_exercise_informations()