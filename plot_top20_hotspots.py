import pandas as pd
import folium
from folium.plugins import HeatMap

# ----------------------------
# 1️⃣ Load CSV
# ----------------------------
# Adjust column names if your CSV differs
df = pd.read_csv('top20_hotspots.csv', names=['city','grid_x','grid_y','total'])

# ----------------------------
# 2️⃣ Reference point for conversion
# ----------------------------
# Suppose you know one grid coordinate matches a real location
# Example: grid_x=1280, grid_y=7745 corresponds to Bengaluru center (12.9716, 77.5946)
known_grid_x = 1280
known_grid_y = 7745
known_lat = 12.9716
known_lon = 77.5946

# Also assume grid origin (0,0) corresponds roughly to:
grid_origin_x = 0
grid_origin_y = 0
# We'll estimate lat_min/lon_min using proportional scaling

# Calculate step sizes (degrees per grid unit)
step_x = (known_lon - 0) / known_grid_x   # longitude per x-grid
step_y = (known_lat - 0) / known_grid_y   # latitude per y-grid

# Optional: if grid origin is not exactly zero, you can adjust lat_min/lon_min
lat_min = 0
lon_min = 0

# ----------------------------
# 3️⃣ Convert all grid coordinates to lat/lon
# ----------------------------
df['lat'] = lat_min + df['grid_y'] * step_y
df['lon'] = lon_min + df['grid_x'] * step_x

# ----------------------------
# 4️⃣ Create a map centered on Bengaluru
# ----------------------------
m = folium.Map(location=[known_lat, known_lon], zoom_start=12)

# ----------------------------
# 5️⃣ Add heatmap layer
# ----------------------------
heat_data = [[row['lat'], row['lon'], row['total']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# ----------------------------
# 6️⃣ Add circle markers
# ----------------------------
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        popup=f"{row['city']} ({row['total']})",
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# ----------------------------
# 7️⃣ Save map
# ----------------------------
m.save('top20_hotspots_map.html')
print("Map saved as top20_hotspots_map.html")
