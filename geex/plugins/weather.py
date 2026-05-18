#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Weather - Display weather information."""

import urllib.request
import json

class WeatherPlugin:
    def __init__(self):
        self.name = "weather"
        self.version = "1.0.0"

    def get_weather(self, location="auto"):
        """Get weather from wttr.in (no API key needed)."""
        try:
            loc = location if location != "auto" else ""
            url = f"https://wttr.in/{loc}?format=%C|%t|%h|%w|%p"
            req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode().strip()
                parts = data.split('|')
                return {
                    'condition': parts[0] if len(parts) > 0 else 'N/A',
                    'temp': parts[1] if len(parts) > 1 else 'N/A',
                    'humidity': parts[2] if len(parts) > 2 else 'N/A',
                    'wind': parts[3] if len(parts) > 3 else 'N/A',
                    'precip': parts[4] if len(parts) > 4 else 'N/A',
                }
        except Exception as e:
            return {'error': str(e), 'condition': 'Unknown', 'temp': 'N/A'}

    def display(self, location="auto"):
        """Display weather."""
        weather = self.get_weather(location)

        if 'error' in weather:
            print(f"\033[93mWeather unavailable: {weather['error']}\033[0m")
            print("\033[94mTip: Make sure you have internet connectivity.\033[0m")
            return

        icons = {
            'Clear': '☀', 'Sunny': '☀', 'Cloudy': '☁',
            'Partly cloudy': '⛅', 'Overcast': '☁',
            'Rain': '🌧', 'Drizzle': '🌦', 'Showers': '🌦',
            'Snow': '🌨', 'Thunderstorm': '⛈', 'Mist': '🌫',
            'Fog': '🌫', 'Haze': '🌫',
        }

        condition = weather.get('condition', 'Unknown')
        icon = icons.get(condition, '🌡')

        print(f"\n  \033[96m{icon}  {condition}\033[0m")
        print(f"  \033[94m🌡 Temperature: \033[97m{weather.get('temp', 'N/A')}\033[0m")
        print(f"  \033[94m💧 Humidity:    \033[97m{weather.get('humidity', 'N/A')}\033[0m")
        print(f"  \033[94m💨 Wind:        \033[97m{weather.get('wind', 'N/A')}\033[0m")
        print("")

def run():
    """Plugin entry point."""
    weather = WeatherPlugin()
    weather.display()

if __name__ == "__main__":
    run()
