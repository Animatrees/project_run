def _is_value_in_range(min_value, max_value, value, coord_name) -> None:
    if not (min_value <= value <= max_value):
        raise ValueError(f'Значение {coord_name} должно находиться в диапазоне от {min_value}° до {max_value}°')


def check_latitude_valid(value) -> None:
    min_value = -90.0
    max_value = 90.0
    coord_name = 'широты'
    _is_value_in_range(min_value, max_value, value, coord_name)


def check_longitude_valid(value) -> None:
    min_value = -180.0
    max_value = 180.0
    coord_name = 'долготы'
    _is_value_in_range(min_value, max_value, value, coord_name)
