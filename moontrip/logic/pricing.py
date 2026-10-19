
"""Round-trip price calculation for the Book page."""

from datetime import date
from numbers import Real


CABIN_MULTIPLIERS = {
    "economy": 1.0,
    "business": 1.8,
    "lunar_suite": 3.0,
}

CHILD_MAX_AGE = 12
SENIOR_MIN_AGE = 65
CHILD_DISCOUNT = 0.50
SENIOR_DISCOUNT = 0.80
REGULAR_DISCOUNT = 1.00


def get_month(travel_date):
    """Parse YYYY-MM-DD and return its month as a string."""
    try:
        parsed_date = date.fromisoformat(travel_date)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "travel_date must be a valid date in YYYY-MM-DD format"
        ) from exc

    # Enforce the exact input format.
    if parsed_date.isoformat() != travel_date:
        raise ValueError("travel_date must use YYYY-MM-DD format")

    return str(parsed_date.month)


def get_cabin_multiplier(cabin):
    """Return the multiplier associated with a cabin."""
    if cabin not in CABIN_MULTIPLIERS:
        raise ValueError(
            f"Invalid cabin: {cabin!r}. "
            f"Choose one of {list(CABIN_MULTIPLIERS)}"
        )

    return CABIN_MULTIPLIERS[cabin]


def get_age_discount(age):
    """Return the fare multiplier based on passenger age."""
    if isinstance(age, bool) or not isinstance(age, int) or age < 0:
        raise ValueError("Passenger age must be a non-negative integer")

    if age < CHILD_MAX_AGE:
        return CHILD_DISCOUNT

    if age >= SENIOR_MIN_AGE:
        return SENIOR_DISCOUNT

    return REGULAR_DISCOUNT


def validate_base_price(base_price):
    """Validate the destination's base one-way price."""
    if (
        isinstance(base_price, bool)
        or not isinstance(base_price, Real)
        or base_price < 0
    ):
        raise ValueError("base_price_inr must be a non-negative number")


def calculate_one_way_fare(base_price, cabin_multiplier, age):
    """Calculate one passenger's discounted one-way fare."""
    age_discount = get_age_discount(age)

    fare = base_price * cabin_multiplier * age_discount
    return round_money(fare)


def calculate_round_trip_fare(base_price, cabin_multiplier, age):
    """Calculate one passenger's discounted round-trip fare."""
    one_way_fare = calculate_one_way_fare(
        base_price, cabin_multiplier, age
    )

    return round_money(one_way_fare * 2)


def round_money(amount):
    """Round a fare to two decimal places."""
    rounded = round(amount, 2)

    # Keep whole-rupee amounts as integers for a clean breakdown.
    if rounded.is_integer():
        return int(rounded)

    return rounded


def calculate_seasonal_surcharge(subtotal, surcharge_pct):
    """Calculate the surcharge on the round-trip subtotal."""
    if (
        isinstance(surcharge_pct, bool)
        or not isinstance(surcharge_pct, Real)
        or surcharge_pct < 0
    ):
        raise ValueError(
            "Seasonal surcharge percentage must be non-negative"
        )

    surcharge = subtotal * surcharge_pct / 100
    return round_money(surcharge)


def trip_price(destination, passengers, cabin, travel_date):
    """Return a breakdown of the round-trip price for all passengers.

    Args:
        destination: Dictionary containing base_price_inr and
            season_surcharge_pct, keyed by month strings "1" through "12".
        passengers: List of dictionaries, each containing an integer age.
        cabin: "economy", "business", or "lunar_suite".
        travel_date: Travel date in YYYY-MM-DD format.

    Returns:
        Dictionary containing passenger fares, subtotal, surcharge,
        and final total.
    """
    if not isinstance(destination, dict):
        raise ValueError("destination must be a dictionary")

    if not isinstance(passengers, list) or not passengers:
        raise ValueError("passengers must be a non-empty list")

    if not isinstance(destination.get("season_surcharge_pct"), dict):
        raise ValueError("season_surcharge_pct must be a dictionary")

    base_price = destination.get("base_price_inr")
    validate_base_price(base_price)

    month = get_month(travel_date)
    cabin_multiplier = get_cabin_multiplier(cabin)

    surcharge_rates = destination["season_surcharge_pct"]
    surcharge_pct = surcharge_rates.get(month)

    if surcharge_pct is None:
        raise ValueError(
            f"Missing seasonal surcharge for month {month}"
        )

    # Calculate each passenger's round-trip fare independently.
    passenger_fares = []

    for passenger in passengers:
        if not isinstance(passenger, dict) or "age" not in passenger:
            raise ValueError(
                "Each passenger must be a dictionary containing age"
            )

        fare = calculate_round_trip_fare(
            base_price=base_price,
            cabin_multiplier=cabin_multiplier,
            age=passenger["age"],
        )
        passenger_fares.append(fare)

    # Apply the seasonal surcharge after all age discounts.
    subtotal = round_money(sum(passenger_fares))
    surcharge = calculate_seasonal_surcharge(
        subtotal, surcharge_pct
    )
    total = round_money(subtotal + surcharge)

    return {
        "passenger_fares_inr": passenger_fares,
        "subtotal_inr": subtotal,
        "surcharge_inr": surcharge,
        "total_inr": total,
    }
