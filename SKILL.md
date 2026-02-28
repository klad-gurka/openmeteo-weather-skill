---
name: weather
description: "Get current weather via Open-Meteo API (actual observations, not forecast). Use when user asks about current weather."
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl", "jq"] } }
---

# Weather Skill (Open-Meteo)

Get ACTUAL current weather - not forecast!

## Locations

| City | Lat | Lon |
|------|-----|-----|
| Göteborg | 57.7089 | 11.9746 |
| Mölndal | 57.6561 | 12.0176 |
| Rävlanda | 57.68 | 12.50 |
| Kungsbacka | 57.4872 | 12.0765 |

## API

```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe/Stockholm"
```

## Weather Codes

| Code | Meaning |
|------|---------|
| 0 | Clear sky ☀️ |
| 1,2,3 | Mainly clear, partly cloudy, overcast ⛅ |
| 45,48 | Fog 🌫️ |
| 51,53,55 | Drizzle 🌧️ |
| 61,63,65 | Rain 🌧️ |
| 71,73,75 | Snow ❄️ |
| 80,81,82 | Rain showers 🌦️ |
| 95 | Thunderstorm ⛈️ |

## Format Message

IMPORTANT: Use the ACTUAL weather code from the API, not a forecast!

Example message:
```
📅 **Dag Datum** - Klockan HH:MM

**Stad:** X.X°C ☁️/☀️/🌧️/🌫️, Vind X m/s, XX% fukt
```

Use the weather CODE (0-99) to pick the right emoji:
- 0 = ☀️
- 1,2,3 = ⛅
- 45,48 = 🌫️
- 51-67,80-82 = 🌧️
- 71-77 = ❄️
- 95+ = ⛈️

## Notes

- Open-Meteo gives CURRENT observations (not forecast)
- Always use the weather_code to pick emoji
- Don't use forecast data - it's often wrong!
