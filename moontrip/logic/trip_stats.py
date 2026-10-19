
"""Aggregate booking statistics for Mission control."""


def get_destination_ids(destinations):
    """Return destination IDs in the supplied destination records."""
    return [
        destination["destination_id"]
        for destination in destinations
    ]


def is_active_booking(booking):
    """Return True when a booking is not cancelled."""
    return booking.get("status") != "cancelled"


def calculate_revenue_by_destination(bookings, destinations):
    """Sum revenue for non-cancelled bookings by destination.

    Destinations with no revenue are included with a value of zero.
    """
    revenue = {
        destination_id: 0
        for destination_id in get_destination_ids(destinations)
    }

    for booking in bookings:
        if not is_active_booking(booking):
            continue

        destination_id = booking["destination_id"]
        total = booking["total_inr"]

        # Also support a booking whose destination is not in the
        # supplied destination list.
        revenue[destination_id] = (
            revenue.get(destination_id, 0) + total
        )

    return revenue


def calculate_bookings_by_status(bookings):
    """Count all bookings by their status."""
    counts = {}

    for booking in bookings:
        status = booking.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1

    return counts


def calculate_average_group_size(bookings):
    """Calculate the mean passenger count across all bookings."""
    if not bookings:
        return 0.0

    total_passengers = sum(
        booking["passenger_count"]
        for booking in bookings
    )

    return round(total_passengers / len(bookings), 2)


def calculate_most_popular_destination(bookings):
    """Find the most frequently booked non-cancelled destination.

    Ties are broken alphabetically by destination_id.
    Return an empty string if there are no non-cancelled bookings.
    """
    destination_counts = {}

    for booking in bookings:
        if not is_active_booking(booking):
            continue

        destination_id = booking["destination_id"]
        destination_counts[destination_id] = (
            destination_counts.get(destination_id, 0) + 1
        )

    if not destination_counts:
        return ""

    # Sort by descending count, then ascending destination ID.
    return min(
        destination_counts,
        key=lambda destination_id: (
            -destination_counts[destination_id],
            destination_id,
        ),
    )


def trip_stats(bookings, destinations):
    """Return aggregate booking statistics for Mission control."""
    if not isinstance(bookings, list):
        raise ValueError("bookings must be a list")

    if not isinstance(destinations, list):
        raise ValueError("destinations must be a list")

    return {
        "revenue_by_destination": calculate_revenue_by_destination(
            bookings, destinations
        ),
        "bookings_by_status": calculate_bookings_by_status(bookings),
        "average_group_size": calculate_average_group_size(bookings),
        "most_popular_destination": (
            calculate_most_popular_destination(bookings)
        ),
    }
