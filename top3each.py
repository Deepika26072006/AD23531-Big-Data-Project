import pandas as pd
import folium

# Load CSV
df = pd.read_csv('top3_spots_per_city.csv', names=['city','grid_x','grid_y','total_crime'])

# Convert total_crime to int safely
df['total_crime'] = pd.to_numeric(df['total_crime'], errors='coerce')
df = df.dropna(subset=['total_crime'])
df['total_crime'] = df['total_crime'].astype(int)

# City base coordinates (for placing the 3 spots around city)
city_coords = {
    'Bengaluru': [12.9716, 77.5946],
    'Delhi': [28.6139, 77.2090],
    'Mumbai': [19.0760, 72.8777],
    'Chennai': [13.0827, 80.2707],
    'Hyderabad': [17.3850, 78.4867]
}

# Assign each city a unique bright color
city_colors = {
    'Bengaluru': "#FF0000",
    'Delhi': "#FFFF00",
    'Mumbai': "#1E90FF",
    'Chennai': "#FFA500",
    'Hyderabad': "#00FF00"
}

# Offsets to show 3 spots around city center
offsets = [[0,0],[0.01,0.01],[0.01,-0.01]]

# Create map
m = folium.Map(location=[21.0, 78.0], zoom_start=5)

# Plot each city's top 3 spots
for city, city_df in df.groupby('city'):
    color = city_colors.get(city, 'gray')
    base_lat, base_lon = city_coords[city]
    
    for i, (_, row) in enumerate(city_df.iterrows()):
        lat = base_lat + offsets[i % 3][0]
        lon = base_lon + offsets[i % 3][1]
        
        # Circle marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)
        
        # Always-visible label
        folium.map.Marker(
            [lat + 0.02, lon],  # slightly above the circle
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 13px;
                    color:{color};
                    font-weight:bold;
                    text-shadow:1px 1px 2px black;
                    text-align:center;
                ">
                    {city}: {row['total_crime']}
                </div>
                """
            )
        ).add_to(m)

# Save map
m.save('top3_hotspots_map.html')
print("✅ Map saved as top3_hotspots_map.html (Top 3 spots per city with visible labels)")
