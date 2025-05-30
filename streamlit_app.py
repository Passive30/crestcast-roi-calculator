
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="CrestCast ROI Calculator", layout="centered")
st.title("CrestCast™ ROI Calculator")
st.markdown("**Quantify the impact of macro-aware investing with Passive 3.0™**")

# --- Inputs ---
aum = st.number_input("Total AUM on Platform ($)", min_value=1_000_000, value=100_000_000, step=1_000_000)
allocation_pct = st.slider("Estimated Allocation to CrestCast Strategy (%)", 0, 100, 50)
overlay_fee = st.number_input("Overlay Fee Charged to Client (bps)", min_value=0.0, value=35.0)
licensing_fee = st.number_input("Licensing Fee to CrestCast (bps)", min_value=0.0, value=15.0)
retention_lift = st.number_input("Client Retention Lift (%)", min_value=0.0, value=10.0)
organic_growth = st.slider("Expected Organic Growth Rate (Annual %)", 0, 50, 25)

# Run simulation button
run_sim = st.button("Run ROI Simulation")

if run_sim:
    # --- Constants ---
    years = 10
    simulations = 100
    base_fee_bps = 10.0

    # Returns and risk assumptions
    crestcast_return = 0.1285
    crestcast_std_dev = 0.1325
    benchmark_return = 0.0968
    benchmark_std_dev = 0.1632

    allocated_aum = aum * (allocation_pct / 100)

    # Monte Carlo Simulations
    crestcast_returns = np.random.normal(crestcast_return, crestcast_std_dev, (simulations, years))
    crestcast_growth = allocated_aum * np.cumprod(1 + crestcast_returns + (organic_growth / 100), axis=1)
    crestcast_median = np.median(crestcast_growth, axis=0)

    benchmark_returns = np.random.normal(benchmark_return, benchmark_std_dev, (simulations, years))
    benchmark_growth = allocated_aum * np.cumprod(1 + benchmark_returns + (organic_growth / 100), axis=1)
    benchmark_median = np.median(benchmark_growth, axis=0)

    # Revenue logic
    crestcast_net_fee_bps = base_fee_bps + overlay_fee - licensing_fee
    benchmark_fee_bps = base_fee_bps
    rev_crestcast = crestcast_median * (crestcast_net_fee_bps / 10000)
    rev_benchmark = benchmark_median * (benchmark_fee_bps / 10000)

    # --- Annual Revenue Bar Chart ---
    st.subheader("Projected Annual Revenue by Year")
    years_range = np.arange(1, years + 1)
    revenue_df = pd.DataFrame({
        "Year": years_range,
        "CrestCast Revenue": rev_crestcast,
        "Benchmark Revenue": rev_benchmark
    })
    st.bar_chart(revenue_df.set_index("Year"))

    # --- Cumulative Revenue Line Chart ---
    st.subheader("Cumulative Revenue Over 10 Years")
    fig, ax1 = plt.subplots()
    ax1.plot(years_range, np.cumsum(rev_crestcast), label="CrestCast", color="blue")
    ax1.plot(years_range, np.cumsum(rev_benchmark), label="Benchmark", color="gray")
    ax1.set_ylabel("Cumulative Revenue ($)")
    ax1.set_xlabel("Year")
    ax1.legend()
    st.pyplot(fig)

    # --- Executive Summary ---
    revenue_lift = np.sum(rev_crestcast - rev_benchmark)
    uplift_pct = (rev_crestcast[-1] - rev_benchmark[-1]) / rev_benchmark[-1] * 100

    st.markdown("### Executive Summary")
    st.markdown(f"✅ **Net Revenue Advantage over 10 years:** ${revenue_lift:,.0f}")
    st.markdown(f"✅ **Year 10 Revenue Uplift:** {uplift_pct:.1f}%")
    st.markdown("✅ **CrestCast Median Return:** 12.85% (Vol: 13.25%)")
    st.markdown("✅ **Benchmark Median Return:** 9.68% (Vol: 16.32%)")
    st.markdown(f"✅ **Net Margin Uplift:** {crestcast_net_fee_bps - benchmark_fee_bps:.1f} bps on allocated AUM")

    st.markdown("---")
    st.markdown("Want to see this for your firm’s client book? **Let’s run a custom analysis.**")
