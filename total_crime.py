import pandas as pd
import folium

# Load the data
df = pd.read_csv('city_crime_summary.csv', names=['city', 'total_crime'])
df['total_crime'] = pd.to_numeric(df['total_crime'], errors='coerce')
df = df.dropna(subset=['total_crime'])

# City coordinates
city_coords = {
    'Bengaluru': [12.9716, 77.5946],
    'Chennai': [13.0827, 80.2707],
    'Delhi': [28.6139, 77.2090],
    'Hyderabad': [17.3850, 78.4867],
    'Mumbai': [19.0760, 72.8777]
}

# Unique bright colors
bright_colors = {
    'Bengaluru': "#FF0000",   # Red
    'Chennai': "#FFA500",     # Orange
    'Delhi': "#FFFF00",       # Yellow
    'Hyderabad': "#00FF00",   # Lime
    'Mumbai': "#1E90FF"       # Blue
}

# Create map centered over India
m = folium.Map(location=[21.0, 78.0], zoom_start=5)

# Plot cities
for _, row in df.iterrows():
    city = row['city']
    total = int(row['total_crime'])

    if city in city_coords:
        lat, lon = city_coords[city]
        color = bright_colors.get(city, "#FFFFFF")

        # Circle marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
        ).add_to(m)

        # Position label (special offset for Bengaluru)
        if city == "Bengaluru":
            label_lat = lat + 0.3
            label_lon = lon - 3.0  # shift left
        else:
            label_lat = lat + 0.4
            label_lon = lon

        # Always visible label
        folium.map.Marker(
            [label_lat, label_lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 14px;
                    color: {color};
                    font-weight: bold;
                    text-shadow: 1px 1px 2px black;
                    text-align: center;
                    white-space: nowrap;
                ">
                    {city}: {total}
                </div>
                """
            )
        ).add_to(m)

# Save map
m.save('city_crime_map_final.html')
print("✅ Map saved as city_crime_map_final.html (Bengaluru label shifted left for clarity)")
