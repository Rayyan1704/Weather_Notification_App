# Import required libraries
import requests  # To fetch weather data from API
import customtkinter as ctk  # Modern GUI framework based on Tkinter
from tkinter import messagebox  # Popup notifications for errors
from plyer import notification  # System notifications (Windows/Mac/Linux)
from config import API_KEY  # API Key stored separately for safety
import threading  # For background auto-refresh feature
import time  # For timing auto-refresh frequency

# Auto-Refresh interval (in seconds): 900s = 15 minutes
REFRESH_INTERVAL = 900  


# ------------------- WEATHER FETCH FUNCTION -------------------
def fetch_weather():
    city = city_input.get()  # Get entered city name

    if city.strip() == "":  # If city name is empty
        messagebox.showwarning("Warning", "Please enter a city name")
        return

    # API URL including city and metric units (Celsius)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)  # Make API Request
        data = response.json()  # Convert response into JSON format

        # Check if API returned valid result
        if data.get("cod") != 200:
            messagebox.showinfo("Warning", "City not found!")
            return

        # Extract required data from API response
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        description = data["weather"][0]["description"].capitalize()

        # Update the app interface with weather results
        result_label.configure(
            text=f"{city.capitalize()} 🌍\n"
                 f"🌡 Temperature: {temp}°C\n"
                 f"💧 Humidity: {humidity}%\n"
                 f"🔽 Pressure: {pressure} hPa\n"
                 f"🌥 Condition: {description}",
        )

        # System notification alert
        notification.notify(
            title=f"Weather Update: {city.capitalize()}",
            message=f"{description} | Temp: {temp}°C | Humidity: {humidity}%",
            timeout=5  # Notification disappears after 5 seconds
        )

    except:
        messagebox.showerror("Error", "Could not fetch weather data!")


# ------------------- AUTO REFRESH THREAD FUNCTION -------------------
def auto_refresh():
    while True:
        time.sleep(REFRESH_INTERVAL)  # Wait 15 mins
        try:
            fetch_weather()  # Refresh weather data automatically
        except:
            pass


def start_auto_refresh():
    # Run auto-refresh in background so GUI does not freeze
    thread = threading.Thread(target=auto_refresh, daemon=True)
    thread.start()


# ------------------- USER INTERFACE DESIGN -------------------

# UI Theme Settings
ctk.set_appearance_mode("Dark")  # Dark Mode UI
ctk.set_default_color_theme("blue")  # Blue accent color

# Main window setup
app = ctk.CTk()
app.title("🌦 Weather Notification App")  # App title
app.geometry("420x350")  # Window size
app.resizable(False, False)  # Disable resizing

# App title label
title_label = ctk.CTkLabel(app, text="🌦 Weather Notification App", font=("Arial", 20, "bold"))
title_label.pack(pady=15)

# Input box for city name
city_input = ctk.CTkEntry(app, width=250, placeholder_text="Enter city name")
city_input.pack(pady=10)

# Button to fetch weather manually
get_btn = ctk.CTkButton(app, text="Get Weather", command=fetch_weather)
get_btn.pack(pady=10)

# Label to show weather results
result_label = ctk.CTkLabel(app, text="", font=("Arial", 15), justify="center")
result_label.pack(pady=15)

# Start auto-refresh in background
start_auto_refresh()

# Run application loop
app.mainloop()
