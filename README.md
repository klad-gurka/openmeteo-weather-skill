# Open-Meteo Weather Skill for OpenClaw

A weather skill that generates beautiful weather report images using the Open-Meteo API and Makin-Things weather icons.

## Features

- 📊 Fetches real-time weather data (not forecast)
- 🖼️ Generates beautiful Discord-ready images
- 🇸🇪 Supports Swedish locations
- 🎨 Uses Makin-Things weather icons
- ⚙️ Easy configuration via config.json

## System Requirements

```bash
# Python dependencies
pip3 install pillow cairosvg

# System dependencies (for CairoSVG)
sudo apt-get install -y librsvg2 python3-cairo
```

## Quick Start

```bash
# Clone the repo
git clone https://github.com/klad-gurka/openmeteo-weather-skill.git
cd openmeteo-weather-skill

# Run
python3 weather-image.py
```

Output is saved to `/tmp/weather-report.png`

## Configuration

All settings are in `config.json`:

```json
{
  "locations": [
    {
      "name": "Göteborg",
      "lat": 57.7089,
      "lon": 11.9746
    },
    {
      "name": "Mölndal", 
      "lat": 57.6561,
      "lon": 12.0176
    },
    {
      "name": "Rävlanda",
      "lat": 57.68,
      "lon": 12.50
    }
  ],
  "settings": {
    "image_width": 1000,
    "image_height": 420,
    "icon_size": 64,
    "title": "Väderrapport"
  }
}
```

### Adding New Locations

Simply add a new entry to the `locations` array in config.json:

```json
{
  "name": "Stockholm",
  "lat": 59.3293,
  "lon": 18.0686
}
```

Then re-run the script - the image will automatically adjust to fit all locations!

### Settings

| Setting | Default | Description |
|---------|---------|-------------|
| image_width | 1000 | Image width in pixels |
| image_height | 420 | Base image height (auto-adjusts) |
| icon_size | 64 | Weather icon size |
| title | "Väderrapport" | Title shown on image |

## Scripts

### weather-image.py (Recommended)

Python script that generates a Discord-ready image with weather icons.

```bash
python3 weather-image.py
# Or with custom config:
python3 weather-image.py /path/to/config.json
```

### weather-report.sh

Simple shell script that outputs weather as plain text (no image).

```bash
bash weather-report.sh
```

Output:
```
📅 **feb 28**

**Göteborg:** ☀️ 6.7°C | 💨 6.5 m/s E | 💧 96%
...
```

## Weather Codes

The script maps WMO weather codes to icons:

| Code | Meaning | Icon |
|------|---------|------|
| 0 | Clear | clear-day |
| 1 | Mainly clear | cloudy-1-day |
| 2 | Partly cloudy | cloudy-2-day |
| 3 | Overcast | cloudy |
| 45, 48 | Fog | fog |
| 51-55 | Drizzle | rainy-1 |
| 61-63 | Rain | rainy-2 |
| 65 | Heavy rain | rainy-3 |
| 71-73 | Snow | snowy-1 |
| 75 | Heavy snow | snowy-3 |
| 80-81 | Rain showers | rainy-2 |
| 82 | Violent rain | rainy-3 |
| 95+ | Thunderstorm | thunderstorms |

## API Sources

### Weather Data
**Open-Meteo API** (free, no key required)
- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Provides actual current weather observations
- No API key needed

### Weather Icons
**Makin-Things Weather Icons**
- GitHub: https://github.com/Makin-Things/weather-icons
- License: MIT
- These icons are based on AmCharts weather icons, updated for Home Assistant

## Icon Attribution

Weather icons are from **[Makin-Things/weather-icons](https://github.com/Makin-Things/weather-icons)** (MIT License).

```
Weather Icons - A set of updated weather icons based of the AmCharts style of icon.
Copyright (c) 2020 Makin' Things
License: MIT - https://github.com/Makin-Things/weather-icons/blob/master/LICENSE
```

## Installation for OpenClaw

1. Copy scripts to your OpenClaw skills folder:
```bash
cp weather-image.py config.json ~/.openclaw/workspace/skills/openmeteo/
```

2. Install dependencies:
```bash
pip3 install pillow cairosvg
sudo apt-get install -y librsvg2
```

3. Configure cron job (example - runs at 7 AM):
```
0 7 * * * python3 ~/.openclaw/workspace/skills/openmeteo/weather-image.py
```

4. The image is saved to `/tmp/weather-report.png` - configure your cron to send it to Discord

## Troubleshooting

### CairoSVG errors
If you get SVG conversion errors, make sure librsvg is installed:
```bash
sudo apt-get install -y librsvg2-bin
```

### Icon download fails
The script downloads icons on first run to `/tmp/makin-icons/`. If it fails:
- Check your internet connection
- Manually download icons from: https://github.com/Makin-Things/weather-icons/tree/master/static

### Config file not found
The script looks for config.json in the same directory as the script. You can also pass the config path as an argument:
```bash
python3 weather-image.py /path/to/config.json
```

## License

- **Weather icons**: [MIT License](https://github.com/Makin-Things/weather-icons/blob/master/LICENSE) (Makin-Things)
- **Scripts**: MIT License (Klåd Gurka)
