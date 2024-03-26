import aiohttp
import asyncio

import pyrainbird.exceptions
import schedule
import time
from datetime import datetime
from pyrainbird import async_client
import requests
import json

from requests import HTTPError, RequestException
from config import *


async def fetch_model_and_version():
    # Create an aiohttp ClientSession
    async with aiohttp.ClientSession() as session:
        # Create an AsyncRainbirdController
        controller = async_client.CreateController(session, RAINBIRD_IP, RAINBIRD_PASSWORD)

        # Fetch the model and version
        model_and_version = await controller.get_model_and_version()
        print(model_and_version)


def get_past_rainfall_adjustment():
    url = "https://api.netatmo.com/getstationsdata"

    try:
        response = requests.get(url, params={'device_id': RAINFALL_DEVICE_ID})
    except (ConnectionError, HTTPError, RequestException) as e:
        print("Error connecting to Netatmo API")
        adjustment_factor = 1
        return adjustment_factor

    response_dict = json.loads(response.text)

    try:
        sum_rain_24 = response_dict['body']['devices'][0]['modules'][0]['oneOf'][0]['dashboard_data']['sum_rain_24']
        print(f"Sum of rain in the last 24 hours: {sum_rain_24} mm")
    except (KeyError, IndexError, TypeError):
        print("Rain gauge data not found or structure is different.")
        sum_rain_24 = 0

    rain_inches = sum_rain_24 / 25.4

    adjustment_factor = 1 - (rain_inches * REDUCTION_PER_INCH)

    adjustment_factor = max(adjustment_factor, 0)

    return adjustment_factor


def irrigation_factor():
    # Get the current month
    current_month = datetime.now().month

    # Get the adjustment factor for the current month
    monthly_factor = monthly_factors.get(current_month, 1.0)

    # Get additional adjustment based on past rainfall
    rainfall_adjustment = get_past_rainfall_adjustment()

    # Combine the monthly factor with the rainfall adjustment
    final_factor = monthly_factor * rainfall_adjustment

    return final_factor


async def irrigate_zone(controller, zone, duration):
    if duration > 0:
        print(f"Starting irrigation for zone {zone} for {duration} minutes. {datetime.now()}")
        await controller.irrigate_zone(zone, duration)
        await asyncio.sleep(duration * 60)  # wait for the duration of irrigation
        print(f"Completed irrigation for zone {zone}. {datetime.now()}")


async def scheduled_irrigation(zone, duration):
    print("asdf")
    async with aiohttp.ClientSession() as client:
        try:
            controller = async_client.CreateController(client, RAINBIRD_IP, RAINBIRD_PASSWORD)
            print(f"Connected to Rainbird Controller for zone {zone}")
            await irrigate_zone(controller, zone, duration)
        except Exception as e:
            print(f"Exception occurred while connecting to Rainbird controller: {e}")


def schedule_irrigation():
    for zone, (days, times) in zone_schedules.items():
        for day in days:
            for time in times:
                schedule.every().day.at(time).do(lambda z=zone, d=base_irrigation_times[zone]: asyncio.run(
                    scheduled_irrigation(z, int(d * irrigation_factor()))))


if __name__ == "__main__":
    try:
        asyncio.run(fetch_model_and_version())
    except pyrainbird.exceptions.RainbirdApiException as e:
        print(f"Could not connect to Rainbird device: {e}")
        exit(1)
    schedule_irrigation()
    print("Irrigation scheduled. Press CTRL+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
