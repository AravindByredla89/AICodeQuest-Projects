
from collections import Counter, defaultdict


def _is_outside_trip(date, trip_start, trip_end):
    """Return whether an activity date falls outside the trip dates."""
    return date < trip_start or date > trip_end


def _activities_overlap(first, second):
    """Check whether two half-open time ranges overlap."""
    return (
        first["start_hour"] < second["end_hour"]
        and second["start_hour"] < first["end_hour"]
    )


def _find_overlaps(activities):
    """Return overlap errors in activity-pair order."""
    errors = []

    for i, first in enumerate(activities):
        for second in activities[i + 1:]:
            if (
                first["date"] == second["date"]
                and _activities_overlap(first, second)
            ):
                errors.append(
                    f'{first["type"]} overlaps with '
                    f'{second["type"]} on {first["date"]}'
                )

    return errors


def _find_excess_moonwalks(activities):
    """Return one error per date with more than two moonwalks."""
    moonwalk_counts = Counter(
        activity["date"]
        for activity in activities
        if activity["type"] == "eva"
    )

    # Preserve the order in which qualifying dates first appear.
    reported_dates = set()
    errors = []

    for activity in activities:
        date = activity["date"]

        if (
            moonwalk_counts[date] > 2
            and date not in reported_dates
        ):
            errors.append(f"more than 2 moonwalks on {date}")
            reported_dates.add(date)

    return errors


def validate_itinerary(activities, trip_start, trip_end):
    """Validate a list of planned trip activities.

    Args:
        activities: List of dictionaries containing type, date,
            start_hour, and end_hour.
        trip_start: Inclusive trip start date (YYYY-MM-DD).
        trip_end: Inclusive trip end date (YYYY-MM-DD).

    Returns:
        An ordered list of validation error messages. Returns an
        empty list when the itinerary passes all specified checks.
    """
    errors = []

    # 1. Activities outside the trip dates.
    for activity in activities:
        date = activity["date"]

        if _is_outside_trip(date, trip_start, trip_end):
            errors.append(
                f"activity on {date} is outside the trip dates"
            )

    # 2. Overlapping activities on the same date.
    errors.extend(_find_overlaps(activities))

    # 3. More than two moonwalks on the same date.
    errors.extend(_find_excess_moonwalks(activities))

    return errors
