import math
async def calculate_radius(lat_start, lon_start, lat_end, lon_end):
    R = 6371000  # Radius Bumi dalam meter

    lat_start_rad = math.radians(lat_start)
    lon_start_rad = math.radians(lon_start)
    lat_end_rad = math.radians(lat_end)
    lon_end_rad = math.radians(lon_end)

    dlat = lat_end_rad - lat_start_rad
    dlon = lon_end_rad - lon_start_rad

    a = math.sin(dlat/2)**2 + math.cos(lat_start_rad) * math.cos(lat_end_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c

    return round(distance, 2) 