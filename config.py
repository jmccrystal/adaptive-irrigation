RAINFALL_DEVICE_ID = ''  # Insert Netatmo rain meter's mac address here
RAINBIRD_IP = ''  # IP address of Rainbird controller
RAINBIRD_PASSWORD = ''  # Password of Rainbird controller
REDUCTION_PER_INCH = 1.0  # Irrigation factor reduced per inch of rain


# Base irrigation times in minutes for each zone
base_irrigation_times = {
    1: 10,
    2: 6,
    5: 15,
    6: 7,
    7: 13,
}

# Dates and times at which sprinkler should run per zone
zone_schedules = {
    1: [("Mon", "Tue", "Thu", "Sat", "Sun"), ("05:45", "13:30")],
    2: [("Tue", "Wed", "Thu", "Sun"), ("05:00", "10:00", "11:00", "14:00", "16:00")],
    5: [("Mon", "Wed", "Thu", "Sat"), ("06:30", "10:30", "12:30")],
    6: [("Mon", "Tue", "Wed", "Thu", "Sat", "Sun"), ("06:00", "09:00", "12:00")],
    7: [("Mon", "Tue", "Thu", "Sat", "Sun"), ("11:30", "15:45")],
}

# Seasonal adjustment factor per month
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

