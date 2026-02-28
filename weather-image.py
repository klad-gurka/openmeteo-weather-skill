#!/usr/bin/env python3
"""Weather report image generator for OpenClaw
Uses Makin-Things SVG weather icons and config.json for locations!
"""
import os
import sys
import json
from datetime import datetime

# Try to import dependencies - install instructions if missing
try:
    from PIL import Image, ImageDraw, ImageFont
    import cairosvg
    import urllib.request
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install: pip3 install pillow cairosvg")
    sys.exit(1)

# Config file path - can be overridden via argument
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + "/config.json"
if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]

# Load config
if not os.path.exists(CONFIG_PATH):
    print(f"Config file not found: {CONFIG_PATH}")
    print("Using default config...")
    config = {
        "locations": [
            {"name": "Göteborg", "lat": 57.7089, "lon": 11.9746},
            {"name": "Mölndal", "lat": 57.6561, "lon": 12.0176},
            {"name": "Rävlanda", "lat": 57.68, "lon": 12.50}
        ],
        "settings": {"title": "Väderrapport"}
    }
else:
    with open(CONFIG_PATH) as f:
        config = json.load(f)

# Get config values
locations = config.get("locations", [])
settings = config.get("settings", {})
title = settings.get("title", "Väderrapport")
img_width = settings.get("image_width", 1000)
img_height = settings.get("image_height", 420)
icon_size = settings.get("icon_size", 64)

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
        except Exception as e:
            print(f"Warning: Could not download {name}: {e}")
            return None
    return Image.open(path).convert("RGBA")

# Preload weather icons
print("Laddar väderikoner...")
weather_icons = {}
for name in ["clear-day", "cloudy-1-day", "cloudy-2-day", "cloudy", "fog", 
             "rainy-1", "rainy-2", "rainy-3", "snowy-1", "snowy-2", "snowy-3", "thunderstorms"]:
    weather_icons[name] = get_icon(name, icon_size)

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
        print(f"Fel vid hämtning av väder för {lat},{lon}: {e}")
        return None

# Wind direction
def get_wind_dir(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    if deg is None: return "N"
    return dirs[int((deg + 22.5) / 45) % 8]

# Calculate image height based on number of locations
row_height = 90
header_height = 100
footer_height = 40
H = header_height + (len(locations) * row_height) + footer_height + 20

# Create image
W = img_width
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

# Title - centered
title_text = f"{title} - {datetime.now().strftime('%d %b')}"
title_w = draw.textlength(title_text, font=font_title)
draw.text(((W - title_w) / 2, 25), title_text, fill='white', font=font_title)

# Column headers
col_y = 85
draw.text((30, col_y), "Stad", fill='#888888', font=font_data)
draw.text((320, col_y), "Temp", fill='#888888', font=font_data)
draw.text((480, col_y), "Vind", fill='#888888', font=font_data)
draw.text((760, col_y), "Fukt", fill='#888888', font=font_data)

# Draw each location
y = header_height
for loc in locations:
    name = loc.get("name", "Unknown")
    lat = loc.get("lat", 0)
    lon = loc.get("lon", 0)
    
    w = get_weather(lat, lon)
    if w:
        icon_name = get_icon_name(w['weather_code'])
        icon = weather_icons.get(icon_name)
        
        # Paste weather icon
        if icon:
            img.paste(icon, (30, y), icon)
        
        # City name
        draw.text((110, y + 15), name, fill='white', font=font_loc)
        
        # Temperature (red)
        temp = f"{w['temperature_2m']:.1f}°C"
        draw.text((320, y + 15), temp, fill='#ff6b6b', font=font_data)
        
        # Wind
        wind = f"{w['wind_speed_10m']:.1f} m/s {get_wind_dir(w['wind_direction_10m'])}"
        if wind_icon:
            img.paste(wind_icon, (480, y + 8), wind_icon)
        draw.text((520, y + 15), wind, fill='#4ecdc4', font=font_data)
        
        # Humidity
        humidity = f"{w['relative_humidity_2m']}%"
        if humidity_icon:
            img.paste(humidity_icon, (760, y + 8), humidity_icon)
        draw.text((800, y + 15), humidity, fill='#45b7d1', font=font_data)
    y += row_height

# Footer
draw.text((30, H - 30), "Ikoner: Makin-Things | Data: Open-Meteo", fill='#666666', font=font_footer)

# Save
output_path = "/tmp/weather-report.png"
img.save(output_path)
print(f"Klar! Saved to {output_path}")
