# Open-Meteo Weather Skill

A weather skill for OpenClaw that uses the Open-Meteo API to get ACTUAL current weather (not forecast).

## Why Open-Meteo?

- ✅ Free, no API key needed
- ✅ Gives REAL observations (not forecast)
- ✅ Fast and reliable
- ✅ Supports Swedish locations

## Weather Codes

Use the `weather_code` from the API to pick the right emoji:

| Code | Meaning | Emoji |
|------|---------|-------|
| 0 | Clear sky | ☀️ |
| 1,2,3 | Mainly clear, partly cloudy, overcast | ⛅ |
| 45,48 | Fog | 🌫️ |
| 51-67,80-82 | Rain | 🌧️ |
| 71-77 | Snow | ❄️ |
| 95+ | Thunderstorm | ⛈️ |

## API Example

```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=57.7089&longitude=11.9746&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe/Stockholm"
```

## Supported Locations

| City | Lat | Lon |
|------|-----|-----|
| Göteborg | 57.7089 | 11.9746 |
| Mölndal | 57.6561 | 12.0176 |
| Rävlanda | 57.68 | 12.50 |
| Kungsbacka | 57.4872 | 12.0765 |

## Install

Copy to your OpenClaw skills folder:
```
~/.openclaw/workspace/skills/openmeteo/
```

## Usage

Ask about weather - the skill will fetch current conditions and format correctly!
