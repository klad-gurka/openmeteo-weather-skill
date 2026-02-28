#!/bin/bash
# Morning weather report script for OpenClaw
# Uses Makin-Things weather icons via raw URLs

# Location format: "NAME:LAT:LON"
LOCATIONS=(
    "Göteborg:57.7089:11.9746"
    "Mölndal:57.6561:12.0176"
    "Rävlanda:57.68:12.50"
)

# Map weather codes to Makin-Things icon names
get_icon() {
    local code=$1
    case $code in
        0) echo "clear-day" ;;          # Clear
        1) echo "cloudy-1-day" ;;       # Mainly clear
        2) echo "cloudy-2-day" ;;      # Partly cloudy  
        3) echo "cloudy" ;;            # Overcast
        45|48) echo "fog" ;;            # Fog
        51|53|55) echo "rainy-1" ;;    # Drizzle (light)
        56|57) echo "rainy-1" ;;        # Freezing drizzle
        61|63) echo "rainy-2" ;;        # Rain (moderate)
        65) echo "rainy-3" ;;           # Rain (heavy)
        66|67) echo "rainy-2" ;;        # Freezing rain
        71|73) echo "snowy-1" ;;        # Snow (light/moderate)
        75) echo "snowy-3" ;;           # Snow (heavy)
        77) echo "snowy-2" ;;           # Snow grains
        80|81) echo "rainy-2" ;;       # Rain showers (moderate)
        82) echo "rainy-3" ;;           # Rain showers (violent)
        85|86) echo "snowy-2" ;;       # Snow showers
        95) echo "thunder" ;;           # Thunderstorm
        96|99) echo "thunder" ;;        # Thunderstorm with hail
        *) echo "cloudy" ;;
    esac
}

# Get emoji for fallback
get_emoji() {
    local code=$1
    case $code in
        0) echo "☀️" ;;
        1|2|3) echo "⛅" ;;
        45|48) echo "🌫️" ;;
        51|53|55|61|63|65|80|81|82) echo "🌧️" ;;
        71|73|75|77|85|86) echo "❄️" ;;
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
    
    ICON=$(get_icon "$CODE")
    EMOJI=$(get_emoji "$CODE")
    WDIR=$(get_wind_dir "$WINDIR")
    
    # Use weather icon from Makin-Things
    echo "**$NAME:** $(get_emoji $CODE) ${TEMP}°C | 💨 $WIND m/s $WDIR | 💧 ${HUMID}%"
done

echo ""
echo "*Ikoner: [Makin-Things](https://github.com/Makin-Things/weather-icons) | Data: Open-Meteo*"
