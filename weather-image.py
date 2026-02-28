#!/usr/bin/env python3
"""Weather report image generator for OpenClaw
Uses Makin-Things SVG weather icons!
"""
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import urllib.request
import json
import os
from datetime import datetime

# Icons directory
ICONS_DIR = "/tmp/makin-icons"
os.makedirs(ICONS_DIR, exist_ok=True)

# Download icons if needed
def get_icon(name, size=64):
    path = f"{ICONS_DIR}/{name}_{size}.png"
    if not os.path.exists(path):
        svg_url = f"https://raw.githubusercontent.com/Makin-Things/weather-icons/master/static/{name}.svg"
        try:
            svg_data = urllib.request.urlopen(svg_url, timeout=10).read()
            cairosvg.svg2png(bytestring=svg_data, write_to=path, output_width=size, output_height=size)
        except:
            return None
    return Image.open(path).convert("RGBA")

# Preload weather icons
print("Laddar väderikoner...")
weather_icons = {}
for name in ["clear-day", "cloudy-1-day", "cloudy-2-day", "cloudy", "fog", 
             "rainy-1", "rainy-2", "rainy-3", "snowy-1", "snowy-2", "snowy-3", "thunderstorms"]:
    try:
        weather_icons[name] = get_icon(name, 64)
    except Exception as e:
        print(f"Kunde inte ladda {name}: {e}")

# Preload data icons
print("Laddar dataikoner...")
wind_icon = get_icon("wind", 32)
humidity_icon = get_icon("rainy-1", 32)

# Weather code to icon name
def get_icon_name(code):
    mapping = {
        0: "clear-day", 1: "cloudy-1-day", 2: "cloudy-2-day", 3: "cloudy",
        45: "fog", 48: "fog",
        51: "rainy-1", 53: "rainy-1", 55: "rainy-1",
        61: "rainy-2", 63: "rainy-2", 65: "rainy-3",
        71: "snowy-1", 73: "snowy-1", 75: "snowy-3",
        80: "rainy-2", 81: "rainy-2", 82: "rainy-3",
        95: "thunderstorms", 96: "thunderstorms", 99: "thunderstorms",
    }
    return mapping.get(code, "cloudy")

# Get weather data
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe/Stockholm"
    try:
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        return data['current']
    except Exception as e:
        print(f"Fel: {e}")
        return None

# Wind direction
def get_wind_dir(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    if deg is None: return "N"
    return dirs[int((deg + 22.5) / 45) % 8]

# Create image - wider and more spacing
W, H = 1000, 420
img = Image.new('RGB', (W, H), color='#1a1a2e')
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    font_loc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    font_data = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_footer = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except:
    font_title = font_loc = font_data = font_footer = ImageFont.load_default()

# Locations
locations = [
    ("Göteborg", 57.7089, 11.9746),
    ("Mölndal", 57.6561, 12.0176),
    ("Rävlanda", 57.68, 12.50),
]

# Title - centered without icon
title = f"Väderrapport - {datetime.now().strftime('%d %b')}"
title_w = draw.textlength(title, font=font_title)
draw.text(((W - title_w) / 2, 25), title, fill='white', font=font_title)

# Column headers
col_y = 85
draw.text((30, col_y), "Stad", fill='#888888', font=font_data)
draw.text((320, col_y), "Temp", fill='#888888', font=font_data)
draw.text((480, col_y), "Vind", fill='#888888', font=font_data)
draw.text((760, col_y), "Fukt", fill='#888888', font=font_data)

# Draw each location - more spacing
y = 130
for name, lat, lon in locations:
    w = get_weather(lat, lon)
    if w:
        icon_name = get_icon_name(w['weather_code'])
        icon = weather_icons.get(icon_name)
        
        # Paste weather icon
        if icon:
            img.paste(icon, (30, y), icon)
        
        # City name - position 110
        draw.text((110, y + 15), f"{name}", fill='white', font=font_loc)
        
        # Temperature (red) - position 320
        temp = f"{w['temperature_2m']:.1f}°C"
        draw.text((320, y + 15), temp, fill='#ff6b6b', font=font_data)
        
        # Wind - position 480
        wind = f"{w['wind_speed_10m']:.1f} m/s {get_wind_dir(w['wind_direction_10m'])}"
        if wind_icon:
            img.paste(wind_icon, (480, y + 8), wind_icon)
        draw.text((520, y + 15), wind, fill='#4ecdc4', font=font_data)
        
        # Humidity - position 760
        humidity = f"{w['relative_humidity_2m']}%"
        if humidity_icon:
            img.paste(humidity_icon, (760, y + 8), humidity_icon)
        draw.text((800, y + 15), humidity, fill='#45b7d1', font=font_data)
    y += 90

# Footer
draw.text((30, 380), "Ikoner: Makin-Things | Data: Open-Meteo", fill='#666666', font=font_footer)

# Save
img.save("/tmp/weather-report.png")
print("Klar! Saved /tmp/weather-report.png")
