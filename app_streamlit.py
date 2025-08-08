import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dumpster Price Lookup", page_icon="🗑️", layout="centered")

@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    else:
        # Fallback to local file if present in the repo
        try:
            df = pd.read_excel("Current-PM-06Aug2025.xlsx", sheet_name="Sheet1")
        except Exception:
            st.info("Upload your Excel file to begin.")
            return None
    # Normalize columns
    df["Zip"] = df["Zip"].astype(str).str.zfill(5)
    if "Client Type" in df.columns:
        df["Client Type"] = df["Client Type"].astype(str)
    return df

st.title("Dumpster Price Lookup")
st.caption("Query pricing by dumpster size, ZIP code, rental period, and client type.")

# Optional file uploader (lets you replace the bundled data without redeploying)
uploaded = st.file_uploader("Upload Excel (.xlsx) — optional", type=["xlsx"], help="If omitted, the app tries to use 'Current-PM-06Aug2025.xlsx' included in the repo.")

df = load_data(uploaded)

if df is None:
    st.stop()

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
            # Price summary
            prices = sorted(results["Client Cost"].dropna().unique().tolist()) if "Client Cost" in results else []
            if prices:
                st.write("**Price(s):** " + ", ".join(f"${int(p)}" if float(p).is_integer() else f"${p}" for p in prices))
            st.dataframe(results, use_container_width=True)

# Helpful meta
with st.expander("About this app"):
    st.markdown("""
- Upload a new Excel to refresh data on the fly (no redeploy needed).
- If multiple rows match (e.g., Standard vs. Elite), all are listed.
- ZIP must be 5 digits.
    """)
