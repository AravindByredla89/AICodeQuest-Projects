
"""Promo code validation and discount calculation."""

from datetime import date
from numbers import Real


PROMO_PERCENT = "percent"
PROMO_FLAT = "flat"


def parse_date(value, field_name):
    """Parse a date string in YYYY-MM-DD format."""
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


def validate_price(price_inr):
    """Ensure the cart price is a non-negative integer."""
    if (
        isinstance(price_inr, bool)
        or not isinstance(price_inr, int)
        or price_inr < 0
    ):
        raise ValueError(
            "price_inr must be a non-negative integer"
        )


def validate_promo_list(promos):
    """Validate the promo collection."""
    if not isinstance(promos, list):
        raise ValueError("promos must be a list")

    for promo in promos:
        if not isinstance(promo, dict):
            raise ValueError("Each promo must be a dictionary")

        if not isinstance(promo.get("code"), str):
            raise ValueError("Each promo must have a string code")

        if promo.get("type") not in (PROMO_PERCENT, PROMO_FLAT):
            raise ValueError(
                f"Invalid promo type for {promo['code']!r}"
            )

        value = promo.get("value")
        if (
            isinstance(value, bool)
            or not isinstance(value, Real)
            or value < 0
        ):
            raise ValueError(
                f"Promo {promo['code']!r} must have a "
                "non-negative numeric value"
            )

        minimum = promo.get("min_spend_inr")
        if (
            isinstance(minimum, bool)
            or not isinstance(minimum, int)
            or minimum < 0
        ):
            raise ValueError(
                f"Promo {promo['code']!r} must have a "
                "non-negative integer min_spend_inr"
            )

        if promo["type"] == PROMO_PERCENT:
            maximum = promo.get("max_discount_inr")
            if (
                isinstance(maximum, bool)
                or not isinstance(maximum, int)
                or maximum < 0
            ):
                raise ValueError(
                    f"Percentage promo {promo['code']!r} must have "
                    "a non-negative integer max_discount_inr"
                )

        parse_date(promo.get("expires"), "expires")


def find_promo(code, promos):
    """Find a promo by exact, case-sensitive code."""
    for promo in promos:
        if promo["code"] == code:
            return promo

    return None


def validate_promo(code, promo, price_inr, today):
    """Return a rejection reason, or None if the promo is eligible."""
    if promo is None:
        return "unknown_code"

    expiry_date = parse_date(promo["expires"], "expires")

    if today > expiry_date:
        return "expired"

    if price_inr < promo["min_spend_inr"]:
        return "below_minimum_spend"

    return None


def calculate_percent_discount(price_inr, promo):
    """Calculate a percentage discount capped at its maximum."""
    discount = round(price_inr * promo["value"] / 100)

    return min(discount, promo["max_discount_inr"])


def calculate_flat_discount(promo):
    """Return the flat promo discount in whole rupees."""
    return round(promo["value"])


def select_best_percent_promo(price_inr, percent_promos):
    """Select the percentage promo giving the largest discount.

    Ties are resolved by promo code alphabetically for deterministic
    results.
    """
    if not percent_promos:
        return None

    return min(
        percent_promos,
        key=lambda promo: (
            -calculate_percent_discount(price_inr, promo),
            promo["code"],
        ),
    )


def apply_promos(price_inr, codes, promos, today):
    """Apply eligible promo codes and return the price breakdown."""
    validate_price(price_inr)

    if not isinstance(codes, list):
        raise ValueError("codes must be a list")

    if any(not isinstance(code, str) for code in codes):
        raise ValueError("Every promo code must be a string")

    validate_promo_list(promos)
    today_date = parse_date(today, "today")

    # Use a canonical date string for consistent date comparisons.
    today = today_date.isoformat()

    accepted = []
    rejected = []

    # Validate every entered code.
    for code in codes:
        promo = find_promo(code, promos)
        reason = validate_promo(code, promo, price_inr, today)

        if reason is not None:
            rejected.append({
                "code": code,
                "reason": reason,
            })
        else:
            accepted.append(promo)

    percent_promos = [
        promo for promo in accepted
        if promo["type"] == PROMO_PERCENT
    ]

    flat_promos = [
        promo for promo in accepted
        if promo["type"] == PROMO_FLAT
    ]

    applied = []
    total_discount = 0

    # Apply only the percentage promo with the largest discount.
    best_percent = select_best_percent_promo(
        price_inr, percent_promos
    )

    if best_percent is not None:
        discount = calculate_percent_discount(
            price_inr, best_percent
        )

        applied.append({
            "code": best_percent["code"],
            "discount_inr": discount,
        })

        total_discount += discount

    # Apply all eligible flat promos.
    for promo in flat_promos:
        discount = calculate_flat_discount(promo)

        applied.append({
            "code": promo["code"],
            "discount_inr": discount,
        })

        total_discount += discount

    # Never allow discounts to reduce the price below zero.
    total_discount = min(total_discount, price_inr)
    final_price = price_inr - total_discount

    # Keep the reported discounts consistent with the actual amount
    # deducted, even when the combined discounts exceed the cart price.
    remaining_discount = price_inr
    adjusted_applied = []

    for item in applied:
        actual_discount = min(
            item["discount_inr"], remaining_discount
        )

        adjusted_applied.append({
            "code": item["code"],
            "discount_inr": actual_discount,
        })

        remaining_discount -= actual_discount

    return {
        "final_price_inr": final_price,
        "applied": adjusted_applied,
        "rejected": rejected,
    }
