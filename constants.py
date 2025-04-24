"""
constants.py
FY 2024‑25 baseline + Budget 2025 proposals.
Flip USE_BUDGET_2025 to False to revert.
"""

USE_BUDGET_2025 = True   # ⇦ set False if proposals not enacted

# New‑Regime slabs
if USE_BUDGET_2025:
    NEW_REGIME_SLABS = [
        (0, 12_00_000, 0.00),
        (12_00_000, 15_00_000, 0.20),
        (15_00_000, float("inf"), 0.30),
    ]
    STD_DEDUCTION_NEW = 75_000
else:
    NEW_REGIME_SLABS = [
        (0, 3_00_000, 0.00), (3_00_000, 6_00_000, 0.05),
        (6_00_000, 9_00_000, 0.10), (9_00_000, 12_00_000, 0.15),
        (12_00_000, 15_00_000, 0.20), (15_00_000, float("inf"), 0.30),
    ]
    STD_DEDUCTION_NEW = 50_000

# Old‑Regime slabs
OLD_REGIME_SLABS = [
    (0, 2_50_000, 0.00),
    (2_50_000, 5_00_000, 0.05),
    (5_00_000, 10_00_000, 0.20),
    (10_00_000, float("inf"), 0.30),
]

# Cess
CESS = 0.04

# Deduction limits (Old Regime)
STD_DEDUCTION_OLD = 50_000
LIM_80C         = 150_000
LIM_80CCD1B     = 50_000
LIM_80D         = 25_000
LIM_24B         = 200_000
LIM_80TTA       = 10_000

# Salary split constants
FOOD_COUPON_ANNUAL = 24_000
LTA_ANNUAL         = 20_000
CAR_LEASE_ANNUAL   = 60_000

# Capital gains & crypto
STCG_RATE       = 0.15
LTCG_FREE_LIMIT = 100_000
LTCG_RATE       = 0.10
CRYPTO_RATE     = 0.30

# ------------------------------------------------------------------
# Back‑compat alias – used by optimizer.py until we refactor it
STD_DEDUCTION = STD_DEDUCTION_OLD
# ------------------------------------------------------------------