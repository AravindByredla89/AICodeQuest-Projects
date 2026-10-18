# ============================================================
# TASK M9 — Luggage fees
# Files for this task:
#   logic/luggage.py            <- this file
#   api/luggage_routes.py
#   web/src/tasks/LuggageEstimator.jsx
# TODO(M9):
#   [ ] implement luggage_fee() in this file
#   [ ] implement the POST /api/luggage/fee route
#   [ ] build the luggage estimator
#   [ ] use an AI assistant; tag its lines honestly in the PR
# ============================================================

def luggage_fee(items, cabin):
    """Return the luggage fee for `items` travelling in `cabin`."""

    # Step 1: Define free luggage allowance for each cabin
    free_allowance = {
        "economy": 5,
        "business": 10,
        "lunar_suite": 20
    }

    # Step 2: Validate cabin
    if cabin not in free_allowance:
        raise ValueError("Invalid cabin type")

    # Step 3: Calculate total weight of non-medical luggage
    total_weight = sum(
        item["weight_kg"]
        for item in items
        if not item["medical"]
    )

    # Step 4: Get free allowance
    free_weight = free_allowance[cabin]

    # Step 5: Calculate excess weight
    excess_weight = max(0, total_weight - free_weight)

    # Step 6: Calculate fee
    # First 5 kg of excess costs Rs. 900/kg
    first_slab = min(excess_weight, 5)

    # Remaining excess costs Rs. 1500/kg
    second_slab = max(0, excess_weight - 5)

    fee = (first_slab * 900) + (second_slab * 1500)

    # Step 7: Return result
    return {
        "total_weight_kg": total_weight,
        "free_weight_kg": free_weight,
        "excess_weight_kg": excess_weight,
        "fee_inr": int(fee)
    }

