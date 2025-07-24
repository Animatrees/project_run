from django.db.models import Sum

from app_run.mappers import get_coordinates_from_run
from app_run.models import Run, Status, Challenge
from app_run.services.geopy_service import get_route_distance


def start_run(run: Run) -> Run:
    if run.status != Status.INIT:
        raise ValueError('Run cannot be started from the current status.')

    run.status = Status.IN_PROGRESS
    run.save()
    return run


def stop_run(run: Run) -> Run:
    if run.status != Status.IN_PROGRESS:
        raise ValueError('Run cannot be finished from the current status.')

    run.status = Status.FINISHED

    coords = get_coordinates_from_run(run)
    distance = get_route_distance(coords)
    run.distance = distance

    run.save()
    _check_challenges(run)
    return run


def _check_challenges(run: Run) -> None:
    _check_ten_runs_challenge(run)
    _check_fifty_km_challenge(run)


def _check_ten_runs_challenge(run: Run) -> None:
    finished_runs = Run.objects.filter(athlete=run.athlete, status=Status.FINISHED).count()
    if finished_runs == 10:
        Challenge.objects.get_or_create(
            full_name='Сделай 10 Забегов!',
            athlete=run.athlete,
        )

def _check_fifty_km_challenge(run: Run) -> None:
    total_distance = Run.objects.filter(athlete=run.athlete, status=Status.FINISHED).aggregate(dist=Sum('distance'))
    if total_distance['dist'] >= 50:
        Challenge.objects.get_or_create(
            full_name='Пробеги 50 километров!',
            athlete=run.athlete,
        )
