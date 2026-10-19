
from datetime import date, datetime, timedelta


def _parse_date(value):
    """Parse a YYYY-MM-DD date string."""
    return datetime.strptime(value, "%Y-%m-%d").date()


def _validate_passenger(passenger, travel_date):
    """Return all validation errors for one passenger."""
    errors = []

    name = passenger.get("name", "")
    age = passenger.get("age")
    medical_clearance = passenger.get("medical_clearance", False)
    passport_expiry = passenger.get("passport_expiry", "")

    # Name is required.
    if not isinstance(name, str) or not name.strip():
        errors.append("name is required")

    # Age must be between 3 and 80 inclusive.
    if (
        isinstance(age, bool)
        or not isinstance(age, int)
        or not 3 <= age <= 80
    ):
        errors.append("age must be between 3 and 80 inclusive")
    elif age >= 70 and medical_clearance is not True:
        errors.append("age 70 or above requires medical clearance")

    # Passport must remain valid for MORE than 180 days
    # after the travel date.
    try:
        expiry_date = _parse_date(passport_expiry)
        if expiry_date <= travel_date + timedelta(days=180):
            errors.append(
                "passport expiry must be more than 180 days "
                "after travel date"
            )
    except (TypeError, ValueError):
        errors.append("passport expiry must be a valid YYYY-MM-DD date")

    return errors


def validate_passengers(passengers, travel_date):
    """Validate passengers for a booking on travel_date.

    Returns a dictionary mapping passenger indices (as strings)
    to lists of validation errors. Passengers without errors
    are omitted.
    """
    parsed_travel_date = _parse_date(travel_date)
    result = {}

    for index, passenger in enumerate(passengers):
        errors = _validate_passenger(passenger, parsed_travel_date)

        if errors:
            result[str(index)] = errors

    return result
