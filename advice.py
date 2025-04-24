"""
advice.py
Generates a ranked list of additional tax‑saving strategies
based on current deductions, income heads and unused limits.
"""

from typing import List, Tuple, Dict
from constants import (
    LIM_80C, LIM_80CCD1B, LIM_80D, LIM_24B,
    LTCG_FREE_LIMIT, STCG_RATE, LTCG_RATE, CRYPTO_RATE
)

def extra_strategies(ded: Dict[str, float],
                     split: Dict[str, float],
                     has_home_loan: bool,
                     stcg: float,
                     ltcg: float,
                     crypto_gain: float,
                     biz_income: float) -> List[Tuple[str, str, str]]:
    """
    Returns list of (Strategy, Potential ₹ Tax Saved, Notes)
    """
    ideas = []

    # --- Core deduction gaps --------------------------------
    gap_80c = LIM_80C - ded.get("80C", 0)
    if gap_80c > 0:
        ideas.append(("Invest ₹{:,} in ELSS/PPF to finish 80C".format(gap_80c),
                      f"₹{gap_80c*0.30:,.0f}", "Instant 30 % saving on amount invested."))

    if ded.get("80CCD1B", 0) == 0:
        ideas.append(("Deposit ₹50,000 in NPS (80CCD 1B)",
                      "₹15,000", "Extra deduction outside 80C."))

    gap_80d = LIM_80D - ded.get("80D", 0)
    if gap_80d > 0:
        ideas.append(("Buy/upgrade health‑insurance (80D)",
                      f"₹{gap_80d*0.30:,.0f}", "Protect family & cut tax."))

    # --- Home‑loan pathway ---------------------------------
    if not has_home_loan:
        ideas.append(("Consider a home loan; up to ₹2 L interest (24b)",
                      "₹60,000", "Combines asset building + tax shield."))

    # --- Capital‑gain planning -----------------------------
    if ltcg > LTCG_FREE_LIMIT:
        ideas.append(("Invest LTCG in 54EC bonds (NHAI/REC) within 6 months",
                      f"₹{(ltcg-LTCG_FREE_LIMIT)*LTCG_RATE:,.0f}",
                      "Locks ₹ up for 5 yrs but avoids 10 % LTCG."))

    # --- Crypto specifics ----------------------------------
    if crypto_gain > 0:
        ideas.append(("Shift crypto trading to FY > optimise FIFO lots",
                      "Variable", "30 % flat tax can’t be avoided but timing reduces impact."))

    # --- 44ADA vs Books ------------------------------------
    if biz_income > 20_00_000:  # heuristic
        ideas.append(("Maintain books & actual expenses instead of presumptive 50 %",
                      "Up to ₹{:,}".format(int(biz_income*0.10)),
                      "If real margin < 50 %, regular P&L may cut tax."))

    # --- HUF route -----------------------------------------
    ideas.append(("Create an HUF & shift future rental / interest income",
                  "Long‑term", "New PAN with separate ₹2.5L zero slab + 80C."))

    # --- Employer benefits ---------------------------------
    if split["Perks"] < 100_000:
        ideas.append(("Ask HR for meal card ↑ or gadget reimbursement",
                      "₹3,000‑10,000", "Fully exempt allowances."))

    return ideas