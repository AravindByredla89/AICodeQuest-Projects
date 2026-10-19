
"""Cancellation and tiered refund calculation."""

from datetime import date


REFUND_TIERS = (
    (30, "flexible", 0.90),
    (7, "standard", 0.50),
    (0, "late", 0.10),
)

MINIMUM_CANCELLATION_FEE_INR = 500
CANCELLATION_FEE_RATE = 0.02


def parse_date(value, field_name):
    """Validate a date string in YYYY-MM-DD format."""
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{field_name} must be a valid YYYY-MM-DD date"
        ) from exc

    if parsed.isoformat() != value:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD format"
        )

    return parsed


def validate_booking(booking):
    """Validate the booking fields required for a refund."""
    if not isinstance(booking, dict):
        raise ValueError("booking must be a dictionary")

    total = booking.get("total_inr")

    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        raise ValueError(
            "total_inr must be a non-negative integer"
        )

    if "launch_date" not in booking:
        raise ValueError("booking must contain launch_date")

    launch_date = parse_date(
        booking["launch_date"], "launch_date"
    )

    return total, launch_date


def days_until_launch(launch_date, cancel_date):
    """Return whole calendar days from cancellation to launch."""
    return (launch_date - cancel_date).days


def get_refund_tier(days_remaining):
    """Return the tier name and refund rate for the cancellation date."""
    if days_remaining > 30:
        return "flexible", 0.90

    if days_remaining >= 8:
        return "standard", 0.50

    if days_remaining >= 1:
        return "late", 0.10

    return "none", 0.0


def calculate_tiered_refund(total_inr, refund_rate):
    """Calculate the refund before deducting the cancellation fee."""
    return round(total_inr * refund_rate)


def calculate_cancellation_fee(total_inr):
    """Return the larger of Rs.500 and 2% of the booking total."""
    percentage_fee = round(
        total_inr * CANCELLATION_FEE_RATE
    )

    return max(
        MINIMUM_CANCELLATION_FEE_INR,
        percentage_fee,
    )


def refund_amount(booking, cancel_date):
    """Return the final refund, cancellation fee, and applicable tier.

    Rules:
    - More than 30 days before launch: 90% refund.
    - 8 to 30 days before launch: 50% refund.
    - 1 to 7 days before launch: 10% refund.
    - Launch day or later: no refund.

    The cancellation fee is the larger of Rs.500 and 2% of the
    booking total, capped at the tiered refund amount.
    """
    total_inr, launch_date = validate_booking(booking)
    cancellation_date = parse_date(cancel_date, "cancel_date")

    remaining_days = days_until_launch(
        launch_date, cancellation_date
    )

    tier, refund_rate = get_refund_tier(remaining_days)

    tiered_refund = calculate_tiered_refund(
        total_inr, refund_rate
    )

    calculated_fee = calculate_cancellation_fee(total_inr)

    # A cancellation fee cannot exceed the available refund.
    fee_inr = min(calculated_fee, tiered_refund)

    final_refund = tiered_refund - fee_inr

    return {
        "refund_inr": final_refund,
        "fee_inr": fee_inr,
        "tier": tier,
    }
