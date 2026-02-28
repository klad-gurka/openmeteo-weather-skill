# Open-Meteo Weather Skill for OpenClaw

A weather skill that generates beautiful weather report images using the Open-Meteo API and Makin-Things weather icons.

## Features

- 📊 Fetches real-time weather data (not forecast)
- 🖼️ Generates beautiful Discord-ready images
- 🇸🇪 Supports Swedish locations
- 🎨 Uses Makin-Things weather icons

## Locations

The skill fetches weather for these Swedish cities:
- Göteborg (57.7089, 11.9746)
- Mölndal (57.6561, 12.0176)
- Rävlanda (57.68, 12.50)

## System Requirements

```bash
# Python dependencies
pip3 install pillow cairosvg

# System dependencies (for CairoSVG)
sudo apt-get install -y librsvg2 python3-cairo
```

## Scripts

### weather-report.sh

Simple shell script that outputs weather as plain text.

```bash
bash weather-report.sh
```

Output example:
```
📅 **feb 28**

**Göteborg:** ☀️ 6.7°C | 💨 6.5 m/s E | 💧 96%
**Mölndal:** ☀️ 6.8°C | 💨 7.6 m/s E | 💧 99%
**Rävlanda:** ☀️ 5.7°C | 💨 4.0 m/s E | 💧 100%

*Data: Open-Meteo*
```

### weather-image.py

Python script that generates a Discord-ready image with weather icons.

```bash
python3 weather-image.py
```

This will:
1. Download weather icons from Makin-Things (first run only)
2. Fetch current weather from Open-Meteo API
3. Generate a nice image with all data
4. Save to `/tmp/weather-report.png`

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

### Icon Attribution

Weather icons are from **[Makin-Things/weather-icons](https://github.com/Makin-Things/weather-icons)** (MIT License).

```
Weather Icons - A set of updated weather icons based of the AmCharts style of icon.
Copyright (c) 2020 Makin' Things
License: MIT - https://github.com/Makin-Things/weather-icons/blob/master/LICENSE
```

## Installation

### For OpenClaw Cron Job

1. Copy scripts to your OpenClaw skills folder:
```bash
cp weather-report.sh ~/.openclaw/workspace/skills/openmeteo/
cp weather-image.py ~/.openclaw/workspace/skills/openmeteo/
```

2. Install dependencies:
```bash
pip3 install pillow cairosvg
sudo apt-get install -y librsvg2
```

3. Configure cron job to run at 7 AM:
```
0 7 * * * python3 /path/to/weather-image.py
```

### Manual Run

```bash
python3 weather-image.py
# Output saved to /tmp/weather-report.png
```

## Output

The image includes:
- Title with current date
- Weather icon for each location
- City name
- Temperature (°C)
- Wind speed and direction
- Humidity (%)
- Footer with data source attribution

## Troubleshooting

### CairoSVG errors
If you get SVG conversion errors, make sure librsvg is installed:
```bash
sudo apt-get install -y librsvg2-bin
```

### Icon download fails
The script downloads icons on first run. If it fails, check your internet connection or manually download from:
https://github.com/Makin-Things/weather-icons/tree/master/static

## License

- **Weather icons**: [MIT License](https://github.com/Makin-Things/weather-icons/blob/master/LICENSE) (Makin-Things)
- **Scripts**: MIT License (Klåd Gurka)
