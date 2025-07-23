from app_run.models import Run
from app_run.services.distance_service import Coordinates


def get_coordinates_from_run(run: Run) -> list[Coordinates]:
    return [Coordinates(lat=float(pos.latitude), lon=float(pos.longitude)) for pos in run.positions.all()]
