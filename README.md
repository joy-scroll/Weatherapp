# Weather Forecast Application

A beautiful and user-friendly weather application that displays real-time weather information based on your current location.

## Features

- Real-time location detection
- Current temperature display
- Weather condition with icon
- Humidity, wind speed, and visibility information
- Beautiful modern UI
- Auto-refresh capability

## Requirements

- Python 3.7 or higher
- Internet connection
- OpenWeatherMap API key

## Installation

1. Clone this repository or download the files
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
4. Replace `YOUR_API_KEY` in `weather_app.py` with your actual API key

## Usage

Run the application:
```bash
python weather_app.py
```

The application will:
1. Automatically detect your location
2. Fetch and display current weather information
3. Show weather details including temperature, humidity, wind speed, and visibility
4. Display weather condition with an appropriate icon

You can click the "Refresh" button to update the weather information manually.

## Note

Make sure you have an active internet connection for the application to work properly. The application requires location services to be enabled on your system. 