# ============================================================
# TASK M11 — Moon Miles loyalty
# Files for this task:
#   logic/loyalty.py            <- this file
#   api/loyalty_routes.py
#   web/src/tasks/LoyaltyCard.jsx
# TODO(M11):
#   [ ] implement loyalty_status() in this file
#   [ ] implement the GET /api/users/<id>/loyalty route
#   [ ] build the loyalty tier card with progress to the next tier
#   [ ] use an AI assistant; tag its lines honestly in the PR
# ============================================================

from datetime import datetime, timedelta


def loyalty_status(bookings, user_id, today):
    """
    Return the Moon Miles balance and tier for user_id.

    Miles are earned only on completed bookings within the
    trailing 365 days, including today.

    Rs. 10 spent = 1 mile.
    """

    # Step 1: Convert today into a date object
    today_date = datetime.strptime(today, "%Y-%m-%d").date()

    # Step 2: Calculate the beginning of the 365-day period
    start_date = today_date - timedelta(days=364)

    # Step 3: Initialize total miles
    total_miles = 0

    # Step 4: Process each booking
    for booking in bookings:

        # Ignore bookings belonging to other users
        if booking["user_id"] != user_id:
            continue

        # Only completed bookings earn miles
        if booking["status"] != "completed":
            continue

        # Convert launch date into date object
        launch_date = datetime.strptime(
            booking["launch_date"], "%Y-%m-%d"
        ).date()

        # Check whether booking falls within trailing 365 days
        if start_date <= launch_date <= today_date:

            # Rs. 10 = 1 mile
            miles = booking["total_inr"] // 10

            total_miles += miles

    # Step 5: Determine loyalty tier
    if total_miles < 5000:
        tier = "Crater"
        next_tier = "Orbit"
        miles_to_next = 5000 - total_miles

    elif total_miles < 20000:
        tier = "Orbit"
        next_tier = "Apollo"
        miles_to_next = 20000 - total_miles

    else:
        tier = "Apollo"
        next_tier = None
        miles_to_next = None

    # Step 6: Return the result
    return {
        "miles": int(total_miles),
        "tier": tier,
        "next_tier": next_tier,
        "miles_to_next": miles_to_next
    }

