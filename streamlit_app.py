
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
base_fee = st.slider("Base Fee Charged to Client (bps)", 0, 25, 10)
overlay_fee = st.number_input("Overlay Fee Charged to Client (bps)", min_value=0.0, value=35.0)
licensing_fee = st.number_input("Licensing Fee to CrestCast (bps)", min_value=0.0, value=15.0)
retention_lift = st.number_input("Client Retention Lift (%)", min_value=0.0, value=10.0)
organic_growth = st.slider("Expected Organic Growth Rate (Annual %)", 0, 50, 25)
tlh_enabled = st.checkbox("Include Tax-Loss Harvesting Uplift?")
tlh_uplift_bps = st.slider("Tax-Loss Harvesting Value (bps)", 0, 10, 5) if tlh_enabled else 0

# --- Benchmark Selector ---
benchmark_choice = st.selectbox("Select Benchmark for Comparison", ["MSCI USA Multi-Factor", "S&P 500"])
benchmark_return = 0.0968 if benchmark_choice == "MSCI USA Multi-Factor" else 0.1153
benchmark_std_dev = 0.1632 if benchmark_choice == "MSCI USA Multi-Factor" else 0.1582

# Run simulation button
run_sim = st.button("Run ROI Simulation")

if run_sim:
    # --- Constants ---
    years = 10
    simulations = 100

    # CrestCast Assumptions
    crestcast_return = 0.1285
    crestcast_std_dev = 0.1325

    allocated_aum = aum * (allocation_pct / 100)

    # Convert fees to decimal form
    crestcast_fee_decimal = (base_fee + overlay_fee - licensing_fee) / 10000
    benchmark_fee_decimal = (base_fee + tlh_uplift_bps) / 10000

    # Simulate returns
    crestcast_returns = np.random.normal(crestcast_return, crestcast_std_dev, (simulations, years))
    benchmark_returns = np.random.normal(benchmark_return, benchmark_std_dev, (simulations, years))

    # Apply fees to returns (net returns)
    crestcast_net_returns = crestcast_returns - crestcast_fee_decimal
    benchmark_net_returns = benchmark_returns - benchmark_fee_decimal

    # Compound net returns (for client index, start at 100)
    client_base = 100
    crestcast_net_growth = client_base * np.cumprod(1 + crestcast_net_returns, axis=1)
    benchmark_net_growth = client_base * np.cumprod(1 + benchmark_net_returns, axis=1)

    # Median values
    crestcast_median_value = np.median(crestcast_net_growth, axis=0)
    benchmark_median_value = np.median(benchmark_net_growth, axis=0)

    # Platform Revenue Calculation (business level includes organic growth)
    crestcast_returns_rev = crestcast_returns + (organic_growth / 100)
    benchmark_returns_rev = benchmark_returns + (organic_growth / 100)

    crestcast_growth_rev = allocated_aum * np.cumprod(1 + crestcast_returns_rev, axis=1)
    benchmark_growth_rev = allocated_aum * np.cumprod(1 + benchmark_returns_rev, axis=1)

    crestcast_median_rev = np.median(crestcast_growth_rev, axis=0)
    benchmark_median_rev = np.median(benchmark_growth_rev, axis=0)

    crestcast_net_fee_bps = base_fee + overlay_fee - licensing_fee
    benchmark_fee_bps = base_fee + tlh_uplift_bps

    rev_crestcast = crestcast_median_rev * (crestcast_net_fee_bps / 10000)
    rev_benchmark = benchmark_median_rev * (benchmark_fee_bps / 10000)

    # --- Annual Revenue Bar Chart ---
    st.subheader("Projected Annual Revenue by Year")
    years_range = np.arange(1, years + 1)
    revenue_df = pd.DataFrame({
        "Year": years_range,
        "CrestCast Revenue": rev_crestcast,
        f"{benchmark_choice} Revenue": rev_benchmark
    })
    st.bar_chart(revenue_df.set_index("Year"))

    # --- Cumulative Revenue Line Chart ---
    st.subheader("Cumulative Revenue Over 10 Years")
    fig1, ax1 = plt.subplots()
    ax1.plot(years_range, np.cumsum(rev_crestcast), label="CrestCast", color="blue")
    ax1.plot(years_range, np.cumsum(rev_benchmark), label=benchmark_choice, color="gray")
    ax1.set_ylabel("Cumulative Revenue ($)")
    ax1.set_xlabel("Year")
    ax1.legend()
    st.pyplot(fig1)

    # --- Client Value Chart (Starting at 100) ---
    st.subheader("Client Index Value (Net of Fees) Over 10 Years")
    fig2, ax2 = plt.subplots()
    ax2.plot(years_range, crestcast_median_value, label="CrestCast (Net of Fees)", color="blue")
    ax2.plot(years_range, benchmark_median_value, label=f"{benchmark_choice} (Net of Fees)", color="gray")
    ax2.set_ylabel("Client Index Value")
    ax2.set_xlabel("Year")
    ax2.legend()
    st.pyplot(fig2)

    # --- Executive Summary ---
    revenue_lift = np.sum(rev_crestcast - rev_benchmark)
    uplift_pct = (rev_crestcast[-1] - rev_benchmark[-1]) / rev_benchmark[-1] * 100

    st.markdown("### Executive Summary")
    st.markdown(f"✅ **Net Revenue Advantage over 10 years:** ${revenue_lift:,.0f}")
    st.markdown(f"✅ **Year 10 Revenue Uplift:** {uplift_pct:.1f}%")
    st.markdown("✅ **CrestCast Median Return:** 12.85% (Vol: 13.25%)")
    st.markdown(f"✅ **{benchmark_choice} Median Return:** {benchmark_return*100:.2f}% (Vol: {benchmark_std_dev*100:.2f}%)")
    st.markdown(f"✅ **Net Margin Uplift:** {crestcast_net_fee_bps - benchmark_fee_bps:.1f} bps on allocated AUM")

    st.markdown("---")
    st.markdown("Want to see this for your firm’s client book? **Let’s run a custom analysis.**")
