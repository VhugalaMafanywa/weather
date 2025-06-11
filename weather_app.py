

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# OpenWeatherMap API setup
API_KEY = "3d900860502d5ec0082fd41b87e2d710"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(event=None):
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    get_weather_btn.config(state='disabled', text="Loading...")
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            raise ValueError(data.get("message", "Unknown error"))

        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        country = data["sys"]["country"]
        
       

        result_label.config(
            text=f"{city.title()}, {country}\n\n"
                 f"Weather: {weather}\n"
                 f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind Speed: {wind} m/s"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather data:\n{e}")
    finally:
        get_weather_btn.config(state='normal', text="Get Weather")



root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.resizable(False, False)


bg_label = tk.Label(root, bg="#e0f7fa")
bg_label.place(relwidth=1, relheight=1)

overlay = tk.Frame(root, bg='white')
overlay.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.8, anchor='n')

title_label = tk.Label(overlay, text="Weather App", font=("Segoe UI", 18, "bold"), bg='white', fg="#333")
title_label.pack(pady=10)

city_entry = tk.Entry(overlay, font=("Segoe UI", 14), justify='center')
city_entry.pack(pady=10, ipadx=5, ipady=5, fill='x', padx=20)
city_entry.bind("<Return>", get_weather)

get_weather_btn = tk.Button(overlay, text="Get Weather", font=("Segoe UI", 12),
                            bg="#3498db", fg="white", command=get_weather)
get_weather_btn.pack(pady=5, fill='x', padx=20)

icon_label = tk.Label(overlay, bg='white')
icon_label.pack(pady=5)

result_label = tk.Label(
    overlay,
    text="",
    font=("Segoe UI", 12),
    bg='white',
    fg="#000",
    justify="left",
    anchor="w",
    wraplength=300  
)
result_label.pack(pady=10, fill='both', padx=20)


root.mainloop()
