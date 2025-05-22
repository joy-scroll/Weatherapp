import customtkinter as ctk
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import json
from PIL import Image, ImageTk
import io
import urllib.request
from datetime import datetime
import time

class WeatherApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Weather Forecast")
        self.window.geometry("800x600")
        self.window.configure(fg_color="#e6f3ff")  # Light blue background
        
        # OpenWeatherMap API key
        self.api_key = "97890fadad986fd772e2e8f75dcb657e"
        
        # Initialize UI components
        self.setup_ui()
        
        # Get initial location and weather
        self.update_weather()
        
    def setup_ui(self):
        # Main frame with vignette effect
        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color="#ffffff",
            corner_radius=20,
            border_width=2,
            border_color="#b3d9ff"  # Light blue border
        )
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Location label
        self.location_label = ctk.CTkLabel(
            self.main_frame,
            text="Detecting location...",
            font=("Helvetica", 28, "bold"),  # Increased font size
            text_color="#333333"
        )
        self.location_label.pack(pady=25)
        
        # Weather icon
        self.weather_icon_label = ctk.CTkLabel(self.main_frame, text="")
        self.weather_icon_label.pack(pady=15)
        
        # Temperature
        self.temp_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 56, "bold"),  # Increased font size
            text_color="#333333"
        )
        self.temp_label.pack(pady=15)
        
        # Weather description
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 22),  # Increased font size
            text_color="#333333"
        )
        self.desc_label.pack(pady=10)
        
        # Weather details frame
        self.details_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#f0f7ff",  # Very light blue
            corner_radius=15,
            border_width=1,
            border_color="#cce5ff"  # Light blue border
        )
        self.details_frame.pack(fill="x", padx=30, pady=25)
        
        # Weather details with increased font sizes
        self.humidity_label = ctk.CTkLabel(
            self.details_frame,
            text="Humidity: --",
            font=("Helvetica", 18),  # Increased font size
            text_color="#333333"
        )
        self.humidity_label.pack(side="left", padx=30)
        
        self.wind_label = ctk.CTkLabel(
            self.details_frame,
            text="Wind: --",
            font=("Helvetica", 18),  # Increased font size
            text_color="#333333"
        )
        self.wind_label.pack(side="left", padx=30)
        
        self.visibility_label = ctk.CTkLabel(
            self.details_frame,
            text="Visibility: --",
            font=("Helvetica", 18),  # Increased font size
            text_color="#333333"
        )
        self.visibility_label.pack(side="left", padx=30)
        
        # Refresh button with updated style
        self.refresh_button = ctk.CTkButton(
            self.main_frame,
            text="Refresh",
            command=self.refresh_weather,
            fg_color="#4a90e2",
            hover_color="#357abd",
            text_color="#ffffff",
            font=("Helvetica", 16, "bold"),  # Increased font size
            corner_radius=10,
            height=40,
            width=120
        )
        self.refresh_button.pack(pady=25)
        
    def get_location(self):
        try:
            # First try to get location from IP
            response = requests.get('https://ipapi.co/json/')
            if response.status_code == 200:
                data = response.json()
                lat = data.get('latitude')
                lon = data.get('longitude')
                city = data.get('city')
                if lat and lon and city:
                    return lat, lon, city
            
            # Fallback to Nominatim if IP geolocation fails
            geolocator = Nominatim(user_agent="weather_app")
            location = geolocator.geocode("me", language="en")
            if location:
                return location.latitude, location.longitude, location.address.split(',')[0]
            
            return None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None
    
    def get_weather(self, lat, lon):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                print(f"Error: {data.get('message', 'Unknown error')}")
                return None
                
            return data
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def refresh_weather(self):
        """Separate method for refresh button"""
        self.location_label.configure(text="Updating...")
        self.temp_label.configure(text="")
        self.desc_label.configure(text="")
        self.humidity_label.configure(text="Humidity: --")
        self.wind_label.configure(text="Wind: --")
        self.visibility_label.configure(text="Visibility: --")
        self.weather_icon_label.configure(image="")
        self.window.update()
        self.update_weather()
    
    def update_weather(self):
        location_data = self.get_location()
        if location_data:
            lat, lon, city = location_data
            weather_data = self.get_weather(lat, lon)
            
            if weather_data:
                try:
                    # Update location
                    self.location_label.configure(text=city)
                    
                    # Update temperature
                    temp = weather_data['main']['temp']
                    self.temp_label.configure(text=f"{temp:.1f}°C")
                    
                    # Update weather description
                    desc = weather_data['weather'][0]['description'].capitalize()
                    self.desc_label.configure(text=desc)
                    
                    # Update weather icon
                    icon_code = weather_data['weather'][0]['icon']
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    icon_data = urllib.request.urlopen(icon_url).read()
                    icon_image = Image.open(io.BytesIO(icon_data))
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    self.weather_icon_label.configure(image=icon_photo)
                    self.weather_icon_label.image = icon_photo
                    
                    # Update details
                    humidity = weather_data['main']['humidity']
                    wind_speed = weather_data['wind']['speed']
                    visibility = weather_data['visibility'] / 1000  # Convert to km
                    
                    self.humidity_label.configure(text=f"Humidity: {humidity}%")
                    self.wind_label.configure(text=f"Wind: {wind_speed} m/s")
                    self.visibility_label.configure(text=f"Visibility: {visibility:.1f} km")
                except KeyError as e:
                    print(f"Error accessing weather data: {e}")
                    self.location_label.configure(text="Error: Invalid weather data format")
                except Exception as e:
                    print(f"Error updating UI: {e}")
                    self.location_label.configure(text="Error updating weather display")
            else:
                self.location_label.configure(text="Error fetching weather data")
        else:
            self.location_label.configure(text="Error detecting location")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
    app.run() 