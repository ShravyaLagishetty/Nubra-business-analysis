# Nubra Market Sizing Analysis - Advanced Attractive Version

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 1. Calculation Function
# -----------------------------
def calculate_market_sizing(students, professionals, smartphone_penetration, adoption_rates, revenue_per_user=2000):
    tam = students + professionals
    sam = int(tam * smartphone_penetration)

    som_results = {}
    revenue_results = {}
    for label, rate in adoption_rates.items():
        som_results[label] = int(sam * rate)
        revenue_results[f"Revenue_{label}"] = som_results[label] * revenue_per_user

    return {"TAM": tam, "SAM": sam, **som_results, **revenue_results}


# -----------------------------
# 2. Generate Sample Dataset
# -----------------------------
def generate_dataset(states, adoption_rates, revenue_per_user):
    data = []
    for state in states:
        students = np.random.randint(200_000, 600_000)
        professionals = np.random.randint(500_000, 1_500_000)
        smartphone_penetration = np.random.uniform(0.5, 0.8)

        results = calculate_market_sizing(students, professionals, smartphone_penetration, adoption_rates, revenue_per_user)
        results["State"] = state
        results["Students"] = students
        results["Professionals"] = professionals
        results["Penetration (%)"] = round(smartphone_penetration * 100, 1)
        data.append(results)

    return pd.DataFrame(data)


# -----------------------------
# 3. Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Nubra Market Sizing", layout="wide")

st.title("Nubra Market Sizing Analysis (Advanced Version)")
st.markdown("""
This interactive tool estimates the *TAM, SAM, SOM, and revenue potential* for Nubra across Indian states.  
You can adjust adoption rates, revenue assumptions, and penetration filters to see how the opportunity changes.  
""")


# -----------------------------
# 4. Sidebar Inputs
# -----------------------------
st.sidebar.header("Adjust Assumptions")

adoption_low = st.sidebar.slider("Adoption Rate (Low %)", 0, 20, 3) / 100
adoption_mid = st.sidebar.slider("Adoption Rate (Medium %)", 0, 20, 5) / 100
adoption_high = st.sidebar.slider("Adoption Rate (High %)", 0, 20, 8) / 100
adoption_rates = {"SOM_Low": adoption_low, "SOM_Medium": adoption_mid, "SOM_High": adoption_high}

revenue_per_user = st.sidebar.number_input("Revenue per User (INR)", min_value=500, max_value=10000, value=2000, step=100)

states = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Kerala",
    "Delhi NCR", "Uttar Pradesh", "Gujarat", "West Bengal", "Punjab"
]

# -----------------------------
# 5. Create Dataset
# -----------------------------
df = generate_dataset(states, adoption_rates, revenue_per_user)

# Filters
selected_states = st.sidebar.multiselect("Select States", states, default=states)
penetration_filter = st.sidebar.slider("Filter by Smartphone Penetration (%)", 50, 80, (50, 80))

filtered_df = df[
    (df["State"].isin(selected_states)) &
    (df["Penetration (%)"] >= penetration_filter[0]) &
    (df["Penetration (%)"] <= penetration_filter[1])
]

# -----------------------------
# 6. Tabs Layout
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Dataset", "Visualizations", "Insights"])

with tab1:
    st.header("Dataset & Filters")
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Dataset", csv, "nubra_market_sizing_filtered.csv", "text/csv")

with tab2:
    st.header("Visualizations")

    # Select a state for detail
    selected_state = st.selectbox("Select a State for Detailed Analysis", filtered_df["State"].unique())
    state_data = filtered_df[filtered_df["State"] == selected_state].iloc[0]

    # Side-by-side charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Market Sizing Breakdown - {selected_state}")
        labels = ["TAM", "SAM", "SOM_Low", "SOM_Medium", "SOM_High"]
        values = [state_data["TAM"], state_data["SAM"], state_data["SOM_Low"], state_data["SOM_Medium"], state_data["SOM_High"]]

        fig, ax = plt.subplots(figsize=(6,4))
        bars = ax.bar(labels, values, color=["#4c72b0", "#55a868", "#c44e52", "#8172b3", "#ccb974"])
        ax.set_ylabel("Number of Engineers")
        ax.set_title("TAM → SAM → SOM Breakdown")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{bar.get_height():,}", ha="center", va="bottom")
        st.pyplot(fig)

    with col2:
        st.subheader("Revenue Projections by State (Medium Adoption)")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.bar(filtered_df["State"], filtered_df["Revenue_SOM_Medium"], color="#4c72b0")
        ax2.set_ylabel("Revenue (INR)")
        ax2.set_title("Revenue Potential by State")
        ax2.set_xticklabels(filtered_df["State"], rotation=45, ha="right")
        st.pyplot(fig2)

    st.subheader("Sensitivity Analysis (Adoption 1–10%)")
    sensitivity = []
    for rate in range(1, 11):
        for state in filtered_df["State"]:
            sam = filtered_df[filtered_df["State"] == state]["SAM"].values[0]
            som = int(sam * (rate / 100))
            sensitivity.append({"State": state, "Adoption (%)": rate, "SOM": som})

    sensitivity_df = pd.DataFrame(sensitivity)
    st.dataframe(sensitivity_df.head(20))

    fig3, ax3 = plt.subplots(figsize=(9,5))
    for state in selected_states:
        state_data_sens = sensitivity_df[sensitivity_df["State"] == state]
        ax3.plot(state_data_sens["Adoption (%)"], state_data_sens["SOM"], marker="o", label=state)
    ax3.set_xlabel("Adoption Rate (%)")
    ax3.set_ylabel("SOM (Engineers)")
    ax3.set_title("SOM Sensitivity to Adoption Rates")
    ax3.legend()
    st.pyplot(fig3)

    csv_sens = sensitivity_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Sensitivity Analysis", csv_sens, "sensitivity_analysis.csv", "text/csv")

with tab3:
    st.header("Insights")

    som_low = state_data.get("SOM_Low", None)
    som_high = state_data.get("SOM_High", None)

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("TAM", f"{state_data['TAM']:,}")
    col2.metric("SAM", f"{state_data['SAM']:,}")
    col3.metric("Revenue (Medium Case)", f"₹{state_data['Revenue_SOM_Medium']:,}")

    st.subheader("Formulas Used")
    st.markdown("""
    - TAM (Total Addressable Market) = Students + Professionals  
    - SAM (Serviceable Available Market) = TAM × Smartphone Penetration (%)  
    - SOM (Serviceable Obtainable Market) = SAM × Adoption Rate (%)  
    - Revenue Projection = SOM × Revenue per User  
    """)

    st.subheader("Calculated Insights")
    if isinstance(som_low, (int, float)) and isinstance(som_high, (int, float)):
        st.success(f"For {selected_state}, Year 1 SOM ranges between {som_low:,} and {som_high:,} engineers.")
    else:
        st.warning("SOM values are missing for this state.")

    st.write("- TAM is the total pool of engineers (students + professionals).")
    st.write("- SAM is the subset with smartphones, internet, and income.")
    st.write("- SOM is Nubra's realistic Year 1 capture, based on adoption.")
    st.write(f"- Revenue is calculated by multiplying SOM by INR {revenue_per_user} per user.")
