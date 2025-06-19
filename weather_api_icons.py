import requests
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# ====== CONFIGURATION ======
API_KEY = "7252717cb4378d0e5d460eb341d2febb"
CSV_FILE = "weather_gui_data.csv"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("message", "Failed to fetch weather data."))
            return

        # Extract icon code and load icon image
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        # Update the icon label
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo  # Keep a reference!

        # Extract and display weather info
        weather = {
            "City": city,
            "Temperature (°C)": data["main"]["temp"],
            "Feels Like (°C)": data["main"]["feels_like"],
            "Weather": data["weather"][0]["description"],
            "Humidity (%)": data["main"]["humidity"],
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        result_text = "\n".join([f"{key}: {value}" for key, value in weather.items()])
        result_label.config(text=result_text)

        # Save to CSV
        try:
            with open(CSV_FILE, "x", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=weather.keys())
                writer.writeheader()
                writer.writerow(weather)
        except FileExistsError:
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=weather.keys())
                writer.writerow(weather)

        messagebox.showinfo("Success", f"Weather data for {city} saved to {CSV_FILE}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ====== GUI SETUP ======
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack()

tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
result_label.pack(pady=10)

root.mainloop()
