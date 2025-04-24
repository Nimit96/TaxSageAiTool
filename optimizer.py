"""
optimizer.py  –  salary optimisation, deductions, investment ideas
v1.2  • supports custom basic%, perk toggles, metro/non‑metro, actual rent
"""

from typing import Dict, List, Tuple
from constants import (
    FOOD_COUPON_ANNUAL, LTA_ANNUAL, CAR_LEASE_ANNUAL,
    STD_DEDUCTION_OLD, LIM_80C, LIM_80CCD1B, LIM_80D, LIM_24B, LIM_80TTA
)

# ──────────────────────────────────────────────────────────────
def salary_split(ctc: float, *,
                 basic_pct: float = 0.40,
                 include_car: bool = True,
                 include_food: bool = True,
                 include_lta: bool = True) -> Dict[str, float]:
    basic   = basic_pct * ctc
    hra     = 0.50 * basic
    pf_emp  = 0.12 * basic
    gratuity= 0.0481 * basic
    perks   = (CAR_LEASE_ANNUAL if include_car else 0) + \
              (FOOD_COUPON_ANNUAL if include_food else 0) + \
              (LTA_ANNUAL if include_lta else 0)
    special = ctc - sum([basic, hra, pf_emp, gratuity, perks])
    return {
        "Basic": round(basic), "HRA": round(hra), "PF_Employer": round(pf_emp),
        "Gratuity": round(gratuity), "Perks": perks, "Special": round(max(0, special))
    }

# ──────────────────────────────────────────────────────────────
def auto_deductions(split: Dict[str, float], *,
                    interest_income: float = 0,
                    invest_80c: float = 0,
                    nps: float = 0,
                    health: float = 0,
                    home_interest: float = 0,
                    actual_rent: float = 0,
                    metro: bool = True) -> Dict[str, float]:

    d = {"Standard": STD_DEDUCTION_OLD}

    epf_employee = split["PF_Employer"]
    d["80C"] = min(LIM_80C, epf_employee + invest_80c)
    d["80CCD1B"] = min(nps, LIM_80CCD1B)
    d["80D"] = min(health, LIM_80D)
    d["80TTA"] = min(interest_income, LIM_80TTA)
    d["24B"] = min(home_interest, LIM_24B)

    # HRA exemption
    mbasic = split["Basic"] / 12
    mhra   = split["HRA"]   / 12
    rent   = actual_rent / 12 if actual_rent else 0.4 * mbasic
    perc   = 0.5 if metro else 0.4
    hra_ex = max(0, min(mhra, rent - 0.10 * mbasic, perc * mbasic) * 12)
    d["HRA_EXEMPT"] = round(hra_ex)

    return d

# ──────────────────────────────────────────────────────────────
def deduction_summary(d: Dict[str, float]) -> Dict[str, Dict]:
    limits = {
        "Standard"   : (STD_DEDUCTION_OLD,     d.get("Standard", 0)),
        "80C"        : (LIM_80C,               d.get("80C", 0)),
        "80CCD1B"    : (LIM_80CCD1B,           d.get("80CCD1B", 0)),
        "80D"        : (LIM_80D,               d.get("80D", 0)),
        "24(b) Home‑loan" : (LIM_24B,          d.get("24B", 0)),
        "80TTA"      : (LIM_80TTA,             d.get("80TTA", 0)),
        "HRA Exemption": ("Varies",            d.get("HRA_EXEMPT", 0))
    }
    table = {}
    for sec, (lim, used) in limits.items():
        gap = "-" if lim == "Varies" else max(0, lim - used)
        table[sec] = {"Max": lim, "Used": used, "Available": gap}
    return table