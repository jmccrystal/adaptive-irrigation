# Rain Bird Smart Irrigation Controller

An automated irrigation control system that interfaces with Rain Bird controllers and adjusts watering schedules based on rainfall data from Netatmo weather stations and seasonal factors.

## Features

- Automated control of Rain Bird irrigation systems
- Integration with Netatmo weather stations for rainfall-based adjustments
- Monthly seasonal adjustments
- Configurable zone-specific schedules
- Automatic rainfall compensation
- Real-time logging of irrigation events

## Prerequisites

- Python 3.7+
- Rain Bird controller with local API access
- Netatmo Weather Station (optional, for rainfall adjustments)

## Required Python Packages

```bash
pip install aiohttp
pip install schedule
pip install pyrainbird
pip install requests
```

## Configuration

Create a `config.py` file with the following settings:

```python
# Rain Bird Controller Settings
RAINBIRD_IP = "your.rainbird.ip"
RAINBIRD_PASSWORD = "your_password"

# Netatmo Settings (if using rainfall adjustment)
RAINFALL_DEVICE_ID = "your_netatmo_device_id"

# Rainfall Adjustment Settings
REDUCTION_PER_INCH = 0.1  # Reduction factor per inch of rain

# Monthly Adjustment Factors (1.0 = 100% of base time)
monthly_factors = {
    1: 0.6,  # January
    2: 0.7,  # February
    3: 0.8,  # March
    # ... Add factors for all months
    12: 0.6  # December
}

# Base Irrigation Times (minutes)
base_irrigation_times = {
    1: 20,  # Zone 1
    2: 15,  # Zone 2
    # ... Add times for all zones
}

# Zone Schedules
zone_schedules = {
    1: (["monday", "wednesday", "friday"], ["06:00"]),
    2: (["tuesday", "thursday", "saturday"], ["07:00"]),
    # ... Add schedules for all zones
}
```

## Usage

Run the irrigation controller:

```bash
python irrigation_controller.py
```

The system will:
1. Connect to your Rain Bird controller
2. Fetch the current model and version
3. Schedule irrigation based on your configuration
4. Continuously monitor and adjust based on rainfall data
5. Log all irrigation events

## How It Works

### Irrigation Scheduling
The system uses the `schedule` library to manage irrigation timing. Each zone can have multiple scheduled times on specified days.

### Rainfall Adjustment
If configured with a Netatmo weather station, the system:
1. Fetches rainfall data for the past 24 hours
2. Adjusts irrigation duration based on recent rainfall
3. Applies a reduction factor per inch of rain

### Seasonal Adjustment
Monthly factors adjust base irrigation times to account for seasonal changes in water needs.

### Final Duration Calculation
Final irrigation duration = Base Time × Monthly Factor × Rainfall Adjustment

## Error Handling

The system includes error handling for:
- Rain Bird controller connection issues
- Netatmo API communication problems
- General execution errors

## Logging

The system logs:
- Irrigation start and end times
- Rainfall measurements
- Connection issues
- Adjustment calculations

## Troubleshooting

1. **Controller Connection Issues**
   - Verify Rain Bird IP address and password
   - Ensure controller is on the same network
   - Check firewall settings

2. **Netatmo Integration Issues**
   - Verify device ID
   - Check internet connectivity
   - Confirm API access

## Contributing

Feel free to submit issues and pull requests for:
- New features
- Bug fixes
- Documentation improvements
- Code optimization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Rain Bird for their irrigation controllers
- Netatmo for their weather station API
- Contributors to the pyrainbird Python package
