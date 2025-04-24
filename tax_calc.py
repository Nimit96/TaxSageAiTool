"""
tax_calc.py
Pure functions that compute taxable income and tax for
Old & New regimes, given aggregated income figures.

Author: AI‑Tax‑Planner
"""

from constants import OLD_REGIME_SLABS, NEW_REGIME_SLABS, CESS

# ──────────────────────────────────────────
# Helper – apply a slab table
def slab_tax(taxable_income: float, slabs: list) -> float:
    """
    taxable_income : total income after deductions (₹)
    slabs          : list of tuples (lower, upper, rate)
    returns        : tax without cess
    """
    tax = 0.0
    for lower, upper, rate in slabs:
        if taxable_income <= lower:
            break
        taxable_segment = min(taxable_income, upper) - lower
        tax += taxable_segment * rate
    return tax


def add_cess(tax: float) -> float:
    """Add 4 % cess."""
    return tax * (1 + CESS)


# ──────────────────────────────────────────
# Public API

def tax_old_regime(taxable: float) -> float:
    """Tax under old slabs + cess."""
    return round(add_cess(slab_tax(taxable, OLD_REGIME_SLABS)))


def tax_new_regime(taxable: float) -> float:
    """Tax under new slabs + cess."""
    return round(add_cess(slab_tax(taxable, NEW_REGIME_SLABS)))