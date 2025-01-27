#from open-meteo.com
import json
import requests
from semantic_kernel.functions import kernel_function

class WeatherPlugin:
    def __init__(self, enableDebug):
        self.enableDebug = enableDebug

    @kernel_function(description="Get the geo coordinates and other location info like: latitude, longitude, elevation, timezone, population, country of a location. Example: get_geocode(location='Rome')")
    async def get_geocode(self, location):
        if self.enableDebug:
            print("START - get_geocode( location=", location, ")")
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                out = json.dumps(data.get("results")[0])
                if self.enableDebug:
                    print("END - get_geocode(",location,"): out=", out)
                return out
        return json.dumps({"location": location, "error": "Unable to fetch geocode"})
    
    @kernel_function(description="Get the meteo forecast for a given latitude and longitude. Example: get_forecast(  latitude=41.8919, longitude=12.5113)")
    async def get_forecast(self, latitude, longitude):
        
        if self.enableDebug:
            print("START - get_forecast( latitude=", latitude, "longitude=", longitude, ")")
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "weather_code", "wind_speed_10m"]
        }
        response = requests.get(url, params=params)

        #print("response.status_code=", response.status_code)
        #print("response=", json.dumps(response.json(), indent=4))

        if response.status_code == 200:
            
            data = response.json()
            if data.get("current"):
                out = json.dumps(data)
                if self.enableDebug:
                    print("END - get_forecast(latitude=", latitude, "longitude=", longitude, "): out=", out)
                return out
        return json.dumps({"latitude=": latitude, "longitude=": longitude, "error": "Unable to fetch geocode"})