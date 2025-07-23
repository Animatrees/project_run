from typing import NamedTuple

from geopy.distance import geodesic


class Coordinates(NamedTuple):
    lat: float
    lon: float


def get_route_distance(coordinates: list[Coordinates]) -> float:
    return geodesic(*coordinates).km
