#!/bin/bash
# Morning weather report script for OpenClaw
# Fetches current weather from Open-Meteo and formats for Discord

# Location format: "NAME:LAT:LON"
LOCATIONS=(
    "Göteborg:57.7089:11.9746"
    "Mölndal:57.6561:12.0176"
    "Rävlanda:57.68:12.50"
)

get_emoji() {
    local code=$1
    case $code in
        0) echo "☀️" ;;
        1|2|3) echo "⛅" ;;
        45|48) echo "🌫️" ;;
        51|53|55|61|63|65|80|81|82) echo "🌧️" ;;
        71|73|75|77) echo "❄️" ;;
        95|96|99) echo "⛈️" ;;
        *) echo "☁️" ;;
    esac
}

get_wind_dir() {
    local dir=$1
    if [ -z "$dir" ]; then echo "N"; fi
    dir=$((dir % 360))
    if [ "$dir" -lt 23 ] || [ "$dir" -ge 338 ]; then echo "N"; 
    elif [ "$dir" -lt 68 ]; then echo "NE";
    elif [ "$dir" -lt 113 ]; then echo "E";
    elif [ "$dir" -lt 158 ]; then echo "SE";
    elif [ "$dir" -lt 203 ]; then echo "S";
    elif [ "$dir" -lt 248 ]; then echo "SW";
    elif [ "$dir" -lt 293 ]; then echo "W";
    elif [ "$dir" -lt 338 ]; then echo "NW";
    else echo "N"; fi
}

# Get today's date
DAY=$(date +%d)
MONTH=$(date +%b)

# Header
echo "📅 **$MONTH $DAY**"
echo ""

# Fetch and display each location
for LOC in "${LOCATIONS[@]}"; do
    IFS=':' read -r NAME LAT LON <<< "$LOC"
    
    DATA=$(curl -s --max-time 10 "https://api.open-meteo.com/v1/forecast?latitude=$LAT&longitude=$LON&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe/Stockholm")
    
    if [ -z "$DATA" ] || [ "$DATA" = "null" ]; then
        echo "**$NAME:** ❌ Fel"
        continue
    fi
    
    TEMP=$(echo "$DATA" | jq -r '.current.temperature_2m')
    HUMID=$(echo "$DATA" | jq -r '.current.relative_humidity_2m')
    WIND=$(echo "$DATA" | jq -r '.current.wind_speed_10m')
    WINDIR=$(echo "$DATA" | jq -r '.current.wind_direction_10m')
    CODE=$(echo "$DATA" | jq -r '.current.weather_code')
    
    EMOJI=$(get_emoji "$CODE")
    WDIR=$(get_wind_dir "$WINDIR")
    
    echo "**$NAME:** $EMOJI ${TEMP}°C | 💨 $WIND m/s $WDIR | 💧 ${HUMID}%"
done

echo ""
echo "*Data: Open-Meteo*"
