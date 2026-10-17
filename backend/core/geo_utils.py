import math
from typing import Tuple, List

# WGS84 ellipsoid constants
WGS84_A = 6378137.0  # semi-major axis in meters
WGS84_E2 = 0.00669437999014  # eccentricity squared

def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance in meters using Haversine formula."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return WGS84_A * c

def wgs84_to_utm43n(lat: float, lon: float) -> Tuple[float, float]:
    """
    Projects WGS84 (lat, lon) to UTM Zone 43N (EPSG:32643) coordinates (easting, northing) in meters.
    Zone 43 central meridian is 75°E.
    """
    lon0 = 75.0
    k0 = 0.9996
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lon0_rad = math.radians(lon0)

    a = WGS84_A
    e2 = WGS84_E2
    e_prime2 = e2 / (1.0 - e2)

    N = a / math.sqrt(1.0 - e2 * (math.sin(lat_rad) ** 2))
    T = math.tan(lat_rad) ** 2
    C = e_prime2 * (math.cos(lat_rad) ** 2)
    A = math.cos(lat_rad) * (lon_rad - lon0_rad)

    # Meridian distance M
    M = a * ((1.0 - e2 / 4.0 - 3.0 * (e2 ** 2) / 64.0 - 5.0 * (e2 ** 3) / 256.0) * lat_rad -
             (3.0 * e2 / 8.0 + 3.0 * (e2 ** 2) / 32.0 + 45.0 * (e2 ** 3) / 1024.0) * math.sin(2.0 * lat_rad) +
             (15.0 * (e2 ** 2) / 256.0 + 45.0 * (e2 ** 3) / 1024.0) * math.sin(4.0 * lat_rad) -
             (35.0 * (e2 ** 3) / 3072.0) * math.sin(6.0 * lat_rad))

    easting = 500000.0 + k0 * N * (A + (1.0 - T + C) * (A ** 3) / 6.0 +
                                   (5.0 - 18.0 * T + T ** 2 + 72.0 * C - 58.0 * e_prime2) * (A ** 5) / 120.0)
    northing = k0 * (M + N * math.tan(lat_rad) * (
        (A ** 2) / 2.0 +
        (5.0 - T + 9.0 * C + 4.0 * (C ** 2)) * (A ** 4) / 24.0 +
        (61.0 - 58.0 * T + T ** 2 + 600.0 * C - 330.0 * e_prime2) * (A ** 6) / 720.0
    ))
    return easting, northing

def polyline_length_m(coords: List[Tuple[float, float]]) -> float:
    """Computes total length of polyline in meters (coords given as [(lat, lon), ...])."""
    if len(coords) < 2:
        return 0.0
    total = 0.0
    for i in range(len(coords) - 1):
        total += haversine_distance_m(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
    return total
