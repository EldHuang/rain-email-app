import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")
MY_LAT = os.environ.get("MY_LAT")
MY_LONG = os.environ.get("MY_LONG")
MY_EMAIL = os.environ.get("MY_EMAIL")
TO_EMAIL = os.environ.get("TO_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "cnt": 4,
}

headers = {
    "appid": api_key
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters, headers=headers)
response.raise_for_status()

weather_data = response.json()

codes = [weather_data["list"][hour]["weather"][0]["id"] for hour in range(len(weather_data["list"]))]
will_rain = any(code < 700 for code in codes)
if will_rain:
    connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=TO_EMAIL,
        msg="Subject: Raining Today\n\nHi Eldridge!\n    It will rain today! Please bring an umbrella to school!\nFrom, Eldridge Python"
    )
else:
    print("hewllo")
