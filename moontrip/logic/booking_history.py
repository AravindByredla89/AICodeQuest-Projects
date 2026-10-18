
# ============================================================
# TASK M3 — Booking history
# ============================================================

from datetime import date


VALID_STATUSES = {"upcoming", "completed", "cancelled"}
VALID_SORT_KEYS = {"launch_date", "total_inr", "destination"}


def _parse_date(value):
    """Convert a YYYY-MM-DD string into a date object."""
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def _get_booking_date(booking):
    """Return the parsed launch date of a booking."""
    return _parse_date(booking.get("launch_date"))


def _matches_user(booking, user_id):
    """Check whether a booking belongs to the requested user."""
    return str(booking.get("user_id")) == str(user_id)


def _matches_status(booking, status):
    """Check whether a booking matches the requested status."""
    if status is None:
        return True

    return booking.get("status") == status


def _matches_from_date(booking, from_date):
    """Apply an inclusive lower bound to the launch date."""
    if from_date is None:
        return True

    booking_date = _get_booking_date(booking)
    minimum_date = _parse_date(from_date)

    if booking_date is None or minimum_date is None:
        return False

    return booking_date >= minimum_date


def filter_bookings(bookings, user_id, status, from_date):
    """Return bookings matching the supplied filters."""
    if status is not None and status not in VALID_STATUSES:
        raise ValueError("Invalid booking status")

    if from_date is not None and _parse_date(from_date) is None:
        raise ValueError("from_date must use YYYY-MM-DD format")

    filtered = []

    for booking in bookings:
        if not _matches_user(booking, user_id):
            continue

        if not _matches_status(booking, status):
            continue

        if not _matches_from_date(booking, from_date):
            continue

        filtered.append(booking)

    return filtered


def _sort_value(booking, key):
    """Extract a normalized value for sorting."""
    if key == "launch_date":
        return _get_booking_date(booking) or date.min

    if key == "total_inr":
        return float(booking.get("total_inr", 0))

    if key == "destination":
        return str(booking.get("destination_id", ""))

    raise ValueError("Invalid booking sort key")


def sort_bookings(bookings, key, descending=False):
    """Sort bookings by a supported key.

    Equal sort-key values are always ordered by ascending booking ID.
    """
    if key not in VALID_SORT_KEYS:
        raise ValueError("Invalid booking sort key")

    # First establish the required ascending-ID tie-break order.
    by_id = sorted(
        bookings,
        key=lambda booking: str(booking.get("id", ""))
    )

    # Python's stable sort preserves ID order for equal sort keys.
    return sorted(
        by_id,
        key=lambda booking: _sort_value(booking, key),
        reverse=descending
    )


def get_booking_by_id(bookings, booking_id):
    """Return a booking by ID, or None if it does not exist."""
    for booking in bookings:
        if str(booking.get("id")) == str(booking_id):
            return booking

    return None


def count_bookings_by_status(bookings, user_id):
    """Count each booking status for one user."""
    counts = {status: 0 for status in VALID_STATUSES}

    for booking in bookings:
        if not _matches_user(booking, user_id):
            continue

        status = booking.get("status")

        if status in counts:
            counts[status] += 1

    return counts


def paginate_bookings(bookings, page=1, page_size=10):
    """Return one page of bookings and pagination metadata."""
    if page < 1:
        raise ValueError("page must be at least 1")

    if page_size < 1:
        raise ValueError("page_size must be at least 1")

    total = len(bookings)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": bookings[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
    }


def search_bookings(bookings, query):
    """Search bookings by booking ID or destination ID."""
    query = str(query or "").strip().lower()

    if not query:
        return list(bookings)

    results = []

    for booking in bookings:
        booking_id = str(booking.get("id", "")).lower()
        destination_id = str(
            booking.get("destination_id", "")
        ).lower()

        if query in booking_id or query in destination_id:
            results.append(booking)

    return results
