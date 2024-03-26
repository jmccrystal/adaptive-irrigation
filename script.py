import aiohttp
import asyncio
import schedule
import time
from datetime import datetime
from pyrainbird import async_client
import requests
import json

from requests import HTTPError, RequestException
from config import *


base_irrigation_times = {
    1: 10,
    2: 6,
    5: 15,
    6: 7,
    7: 13,
}

zone_schedules = {
    1: [("Mon", "Tue", "Thu", "Sat", "Sun"), ("05:50", "13:30")],
    2: [("Tue", "Wed", "Thu", "Sun"), ("05:00", "10:00", "11:00", "14:00", "16:00")],
    5: [("Mon", "Wed", "Thu", "Sat"), ("06:30", "10:30", "12:30")],
    6: [("Mon", "Tue", "Wed", "Thu", "Sat", "Sun"), ("06:00", "09:00", "12:00")],
    7: [("Mon", "Tue", "Thu", "Sat", "Sun"), ("11:30", "15:50")],
}

monthly_factors = {
    1: 0.5,  # January
    2: 0.5,  # February
    3: 0.6,  # March
    4: 0.7,  # April
    5: 0.8,  # May
    6: 1.0,  # June
    7: 1.0,  # July
    8: 1.0,  # August
    9: 0.8,  # September
    10: 0.7,  # October
    11: 0.5,  # November
    12: 0.5  # December
}


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
    async with aiohttp.ClientSession() as client:
        controller = async_client.CreateController(client, RAINBIRD_IP, RAINBIRD_PASSWORD)
        print(f"Connected to Rainbird Controller for zone {zone}")
        await irrigate_zone(controller, zone, duration)


def schedule_irrigation():
    for zone, (days, times) in zone_schedules.items():
        for day in days:
            for time in times:
                schedule.every().day.at(time).do(lambda z=zone, d=base_irrigation_times[zone]: asyncio.run(
                    scheduled_irrigation(z, int(d * irrigation_factor()))))


if __name__ == "__main__":
    schedule_irrigation()
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
