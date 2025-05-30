
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(page_title="CrestCast ROI Calculator", layout="centered")

st.title("CrestCast™ ROI Calculator")
st.markdown("**Quantify the impact of macro-aware investing with Passive 3.0™**")

# --- Inputs ---
aum = st.number_input("Total AUM on Platform ($)", min_value=1_000_000, value=100_000_000, step=1_000_000)
allocation_pct = st.slider("Estimated Allocation to CrestCast Strategy (%)", 0, 100, 50)
client_fee = st.number_input("Client Fee (bps)", min_value=0.0, value=35.0)
licensing_fee = st.number_input("Licensing Fee to CrestCast (bps)", min_value=0.0, value=15.0)
retention_lift = st.number_input("Client Retention Lift (%)", min_value=0.0, value=10.0)

# --- Constants ---
years = 10
crestcast_return = 0.1285
benchmark_return = 0.0968

# --- Computations ---
allocated_aum = aum * (allocation_pct / 100)
aum_retained_bonus = allocated_aum * (retention_lift / 100)

# AUM growth over time
years_range = np.arange(1, years + 1)
aum_crestcast = allocated_aum * (1 + crestcast_return) ** years_range + aum_retained_bonus
aum_benchmark = allocated_aum * (1 + benchmark_return) ** years_range

# Revenue calculations
client_fee_decimal = client_fee / 10000
licensing_fee_decimal = licensing_fee / 10000
rev_crestcast = aum_crestcast * (client_fee_decimal - licensing_fee_decimal)
rev_benchmark = aum_benchmark * client_fee_decimal

# --- Charts ---
st.subheader("Annual Revenue Comparison (Final Year)")
st.bar_chart({
    "CrestCast": [rev_crestcast[-1]],
    "Benchmark": [rev_benchmark[-1]]
})

st.subheader("Cumulative Revenue Over 10 Years")
fig, ax1 = plt.subplots()
ax1.plot(years_range, np.cumsum(rev_crestcast), label="CrestCast", color="blue")
ax1.plot(years_range, np.cumsum(rev_benchmark), label="Benchmark", color="gray")
ax1.set_ylabel("Cumulative Revenue ($)")
ax1.set_xlabel("Year")
ax1.legend()
st.pyplot(fig)

# --- Summary ---
st.markdown(f"**Net Revenue Advantage over 10 years:** ${np.sum(rev_crestcast - rev_benchmark):,.0f}")
st.markdown("Results are based on historical return assumptions from 2015–2025 performance data.")
