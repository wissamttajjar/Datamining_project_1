import numpy as np
import pandas as pd


def calculate_price(row):
    base_fare = 3.59 if row['member_casual'] == 'member' else 1.00

    overage_minutes = max(0, row['duration_min'] - 45)
    if row['rideable_type'].lower() == 'electric':
        time_charge = 0.15 * overage_minutes
    else:
        time_charge = 0.05 * overage_minutes

    mall_tax = 0.5 if row['start_near_any_mall'] == 1 or row['end_near_any_mall'] == 1 else 0.0

    long_trip_tax = 3.0 if row['duration_min'] > 1440 else 0.0

    return round(base_fare + time_charge + mall_tax + long_trip_tax, 2)


def fill_from_start_coords(row, col, ref_from_start):
    key = (row['rounded_start_lat'], row['rounded_start_lon'])
    if pd.isna(row[col]) and key in ref_from_start.index:
        return ref_from_start.loc[key, col]
    return row[col]


def haversine_np(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2.0) ** 2 + \
        np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def distance_to_closest_mall(lat, lon, shopping_centers):
    if np.isnan(lat) or np.isnan(lon):
        return np.nan
    distances = haversine_np(lat, lon, shopping_centers[:, 0], shopping_centers[:, 1])
    return np.min(distances)


def classify_weather(condition):
    if pd.isna(condition):
        return np.nan
    condition = condition.lower()
    if any(w in condition for w in ['clear', 'sunny']):
        return 'Sunny'
    elif any(w in condition for w in ['rain', 'storm', 'shower', 'drizzle']):
        return 'Rainy'
    elif any(w in condition for w in ['cloud', 'overcast', 'fog', 'mist']):
        return 'Cloudy'
    else:
        return 'Cloudy'
