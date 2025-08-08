
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Dumpster Price Lookup", page_icon="🗑️", layout="centered")

# ---- CONFIG ----
# Put your Excel in the same folder as this file OR in a ./data subfolder.
FILENAME = "Current-PM-06Aug2025.xlsx"
CANDIDATE_PATHS = [
    Path(__file__).parent / FILENAME,
    Path(__file__).parent / "data" / FILENAME,
]

def find_file():
    for p in CANDIDATE_PATHS:
        if p.exists():
            return p
    return None

@st.cache_data(show_spinner=False)
def load_data(path: Path):
    df = pd.read_excel(path, sheet_name="Sheet1")
    df["Zip"] = df["Zip"].astype(str).str.zfill(5)
    if "Client Type" in df.columns:
        df["Client Type"] = df["Client Type"].astype(str)
    return df

st.title("Dumpster Price Lookup")
st.caption("Uses the Excel file bundled in this repository. No upload required.")

excel_path = find_file()
if not excel_path:
    st.error(
        "Excel file not found. Please add **Current-PM-06Aug2025.xlsx** to the repo root "
        "or to a **data/** folder, then redeploy."
    )
    st.stop()

st.success(f"Loaded data from: `{excel_path.name}`")

df = load_data(excel_path)

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    size = st.selectbox("Dumpster Size (yards)", sorted(df["Size"].dropna().unique().tolist()))
    rental = st.selectbox("Rental Period (days)", sorted(df["Rental Length"].dropna().unique().tolist()))
    client = st.selectbox("Client Type", sorted(df["Client Type"].dropna().unique().tolist()))
    zip_code = st.text_input("ZIP Code", max_chars=5, placeholder="e.g., 02139")

lookup = st.button("Get Price")

if lookup:
    if not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        st.error("Please enter a valid 5-digit ZIP code.")
    else:
        mask = (
            (df["Size"] == size) &
            (df["Rental Length"] == rental) &
            (df["Client Type"].str.lower() == str(client).lower()) &
            (df["Zip"] == zip_code)
        )
        cols = ["Zip", "Zone", "Category", "Pricing Type", "Weight Allowance in Tons",
                "Client Cost", "Cost per Day Over", "Delivery Fee", "Cost per Ton Over"]
        results = df.loc[mask, [c for c in cols if c in df.columns]].copy()

        if results.empty:
            st.warning("No matching price found for the given inputs.")
        else:
            st.success(f"Found {len(results)} match(es).")
            prices = sorted(results["Client Cost"].dropna().unique().tolist()) if "Client Cost" in results else []
            if prices:
                st.write("**Price(s):** " + ", ".join(f"${int(p)}" if float(p).is_integer() else f"${p}" for p in prices))
            st.dataframe(results, use_container_width=True)

with st.expander("Troubleshooting"):
    st.markdown(
        "- Ensure the Excel file name is exactly **Current-PM-06Aug2025.xlsx** (case-sensitive).\n"
        "- Place it next to `app_streamlit_repo.py` or in a `data/` subfolder.\n"
        "- Commit & push to GitHub, then redeploy the app."
    )
