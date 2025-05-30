
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
overlay_fee = st.number_input("Overlay Fee Charged to Client (bps)", min_value=0.0, value=35.0)
licensing_fee = st.number_input("Licensing Fee to CrestCast (bps)", min_value=0.0, value=15.0)
retention_lift = st.number_input("Client Retention Lift (%)", min_value=0.0, value=10.0)

# --- Constants ---
years = 10
crestcast_return = 0.1285
benchmark_return = 0.0968
base_fee_bps = 10.0

# --- Computations ---
allocated_aum = aum * (allocation_pct / 100)

# Apply retention lift annually (as a compounding retention benefit)
years_range = np.arange(1, years + 1)
aum_crestcast = [allocated_aum]
aum_benchmark = [allocated_aum]

for year in years_range[1:]:
    prev_crestcast = aum_crestcast[-1]
    prev_benchmark = aum_benchmark[-1]
    aum_crestcast.append(prev_crestcast * (1 + crestcast_return + (retention_lift / 100)))
    aum_benchmark.append(prev_benchmark * (1 + benchmark_return))

aum_crestcast = np.array(aum_crestcast)
aum_benchmark = np.array(aum_benchmark)

# Revenue in basis points
crestcast_net_fee_bps = base_fee_bps + overlay_fee - licensing_fee
benchmark_fee_bps = base_fee_bps

rev_crestcast = aum_crestcast * (crestcast_net_fee_bps / 10000)
rev_benchmark = aum_benchmark * (benchmark_fee_bps / 10000)

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
st.markdown("Results based on historical return assumptions from 2015–2025 performance data.")
