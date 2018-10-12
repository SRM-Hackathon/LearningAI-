from datetime import timedelta

from django.utils import timezone


def get_displaced_time_from_duration_entity(current_time, duration):
    duration_magnitude = duration["amount"]
    unit = duration["unit"]
    if unit == 'h':
        displaced_time = current_time + timedelta(hours=duration_magnitude)
    elif unit == 'm':
        displaced_time = current_time + timedelta(minutes=duration_magnitude)
    else:
        displaced_time = current_time + timedelta(days=duration_magnitude)
    return displaced_time
