# app.py  –  Tax Sage AI v1.2
# Complete Streamlit dashboard with expanded tweaks & deduction gaps

import streamlit as st, pandas as pd, altair as alt
from constants  import *
from optimizer  import salary_split, auto_deductions, deduction_summary
from tax_calc   import tax_old_regime, tax_new_regime
from advice     import extra_strategies

st.set_page_config(page_title="Tax Sage AI", page_icon="🦉")
st.title("🦉 Tax Sage AI — FY 2024‑25 (Budget 2025 rules)")

if USE_BUDGET_2025:
    st.toast("Budget 2025: New Regime zero‑tax up to ₹12 L, std ded ₹75 k.", icon="👍")

# ─── Quick inputs ────────────────────────────────────────────
st.sidebar.header("Just five numbers")
salary_ctc = st.sidebar.number_input("Salary CTC (₹)", 0, step=50_000)
biz_income = st.sidebar.number_input("Freelance Income (₹)", 0, step=50_000)
cap_gain   = st.sidebar.number_input("Total Capital Gains (₹)", 0, step=50_000)
crypto_g   = st.sidebar.number_input("Crypto Gains (₹)", 0, step=50_000)
rental_g   = st.sidebar.number_input("Rental Income (₹)", 0, step=50_000)

# ─── Advanced options ───────────────────────────────────────
with st.sidebar.expander("Advanced options"):
    st.markdown("###### Salary structure")
    basic_pct = st.slider("Basic salary % of CTC", 30, 50, 40) / 100
    metro     = st.checkbox("Metro city (HRA)", True)
    actual_rent = st.number_input("Actual rent (₹/yr)", 0, step=10_000)
    perks_car  = st.checkbox("Car‑lease benefit", True)
    perks_food = st.checkbox("Meal card", True)
    perks_lta  = st.checkbox("LTA", True)

    st.markdown("###### Deduction inputs")
    home_int = st.number_input("Home‑loan interest (₹)", 0, step=50_000)
    health_p = st.number_input("Health‑insurance premium (₹)", 0, step=5_000)
    nps_paid = st.number_input("NPS contribution (₹)", 0, step=10_000)

    st.markdown("###### Capital‑gain split")
    lt_pct = st.slider("LTCG portion of total gains (%)", 0, 100, 80)

# ─── Salary split & deductions ──────────────────────────────
split = salary_split(
    salary_ctc,
    basic_pct=basic_pct,
    include_car=perks_car,
    include_food=perks_food,
    include_lta=perks_lta
)

ded = auto_deductions(
    split,
    nps=nps_paid,
    health=health_p,
    home_interest=home_int,
    actual_rent=actual_rent,
    metro=metro
)

# Capital‑gain decomposition
stcg = cap_gain * (1 - lt_pct / 100)
ltcg = cap_gain * (lt_pct / 100)
stcg_tax  = stcg * STCG_RATE
ltcg_tax  = max(0, (ltcg - LTCG_FREE_LIMIT) * LTCG_RATE)
crypto_tax = crypto_g * CRYPTO_RATE

# Tax calculations
salary_tax_old = max(0, salary_ctc - split["PF_Employer"] - sum(ded.values()))
biz_taxable    = 0.5 * biz_income
rent_taxable   = max(0, rental_g * 0.70)
taxable_old    = salary_tax_old + biz_taxable + rent_taxable
tax_old = tax_old_regime(taxable_old) + stcg_tax + ltcg_tax + crypto_tax

salary_tax_new = salary_ctc - split["PF_Employer"] - STD_DEDUCTION_NEW
taxable_new    = salary_tax_new + biz_income + rental_g
tax_new = tax_new_regime(taxable_new) + stcg_tax + ltcg_tax + crypto_tax

better = "Old Regime" if tax_old < tax_new else "New Regime"

# ─── Top summary ────────────────────────────────────────────
st.header("Regime comparison")
c1, c2 = st.columns(2)
c1.metric("Tax – Old", f"₹{tax_old:,.0f}")
c2.metric("Tax – New", f"₹{tax_new:,.0f}")
st.success(f"**Recommended:** {better}")

take_home = (salary_ctc + biz_income + rental_g
             - (tax_old if better == 'Old Regime' else tax_new)) / 12
st.subheader(f"Estimated monthly take‑home: **₹{take_home:,.0f}**")

# ─── Tabs ───────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Salary split",
    "Deduction capacity",
    "Master playbook"
])

with tab1:
    st.markdown("#### Optimised salary components")
    st.table(pd.Series(split, name="₹").apply(lambda x: f"₹{x:,.0f}"))

with tab2:
    st.markdown("#### Current vs maximum deductions")
    df_ded = pd.DataFrame(deduction_summary(ded)).T
    
    # Convert the columns to numeric, ensuring we handle errors gracefully
    df_ded["Max"] = pd.to_numeric(df_ded["Max"], errors='coerce')
    df_ded["Used"] = pd.to_numeric(df_ded["Used"], errors='coerce')
    df_ded["Available"] = pd.to_numeric(df_ded["Available"], errors='coerce')

    # Convert all values to string with currency format for display
    df_ded["Max"] = df_ded["Max"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "₹0")
    df_ded["Used"] = df_ded["Used"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "₹0")
    df_ded["Available"] = df_ded["Available"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "₹0")

    # Display the formatted DataFrame without the styling
    st.dataframe(df_ded)

with tab3:
    st.markdown("#### Additional tax‑saving strategies")
    strategies = extra_strategies(
        ded, split,
        has_home_loan=home_int > 0,
        stcg=stcg, ltcg=ltcg, crypto_gain=crypto_g, biz_income=biz_income
    )
    df_strat = pd.DataFrame(strategies,
                            columns=["Strategy", "Est. ₹ Tax Saved", "Why / Caveat"])
    st.table(df_strat)

# Footer
st.caption("Crypto gains taxed @ 30 % · LT/STCG as per Sec 112A/111A · 4 % cess applied")