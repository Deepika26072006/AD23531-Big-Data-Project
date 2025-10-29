import csv, random, uuid, datetime

random.seed(44)

# Configuration from your JSON schema
cities = ["Bengaluru", "Chennai", "Mumbai", "Delhi", "Hyderabad"]
city_weights = [3,2,2,2,1]

sensor_types = ["air_quality", "traffic", "noise", "water"]
sensor_weights = [4,3,2,1]

lat_min, lat_max = 12.8, 13.1
lon_min, lon_max = 77.45, 77.8

start_date = datetime.datetime(2025, 1, 1, 6, 0, 0)
end_date = datetime.datetime(2025, 2, 28, 23, 59, 59)
delta_seconds = int((end_date - start_date).total_seconds())

# Output CSV
filename = "crimes.csv"
rows = 200000

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["event_id","event_time","city","sensor_type","latitude","longitude","pm25","noise_db","traffic_flow","incident_flag","key"])
    
    for _ in range(rows):
        event_id = str(uuid.uuid4())
        # weighted time (simple uniform plus peak hours)
        event_time = start_date + datetime.timedelta(seconds=random.randint(0, delta_seconds))
        
        city = random.choices(cities, weights=city_weights)[0]
        sensor = random.choices(sensor_types, weights=sensor_weights)[0]
        
        lat = round(random.uniform(lat_min, lat_max), 4)
        lon = round(random.uniform(lon_min, lon_max), 4)
        
        # pm25 lognormal
        pm25 = round(random.lognormvariate(3.0, 0.6),2)
        # noise_db normal
        noise_db = round(random.gauss(65, 10),2)
        # traffic_flow
        traffic_flow = int(random.triangular(0,5000,5000*0.5))  # skew ~1.1
        # incident_flag
        incident_flag = 1 if random.random() < 0.02 else 0
        # derived key
        key = f"{sensor}|{city}"
        
        writer.writerow([event_id, event_time.isoformat(), city, sensor, lat, lon, pm25, noise_db, traffic_flow, incident_flag, key])

print(f"✅ Generated {rows} rows in {filename}")
