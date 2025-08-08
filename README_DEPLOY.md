# Dumpster Price Lookup — Web App (Streamlit)

### Option A — Deploy on Streamlit Community Cloud (free, easiest)
1) Create a **GitHub** repo and add:
   - `app_streamlit.py`
   - `requirements_streamlit.txt`
   - (Optional) `Current-PM-06Aug2025.xlsx` if you want the app to load a default dataset.
2) Go to https://share.streamlit.io, connect your GitHub, and choose the repo & branch.
3) Set **Main file path** to `app_streamlit.py`. Deploy.
4) You’ll get a public URL like `https://your-app.streamlit.app/`.
   - You can also upload a new Excel file from the app UI at any time.

### Option B — Self-host
1) On a server (or your machine), install Python 3.9+
2) `pip install -r requirements_streamlit.txt`
3) Place `Current-PM-06Aug2025.xlsx` next to `app_streamlit.py` (or upload via the UI after launch)
4) Run: `streamlit run app_streamlit.py --server.port 8501 --server.address 0.0.0.0`
5) Open `http://<server-ip>:8501`

### Notes
- The app reads the `Sheet1` tab and normalizes ZIP codes to 5 digits.
- If you include the Excel file in the repo, it loads automatically. Otherwise, use the **Upload** control.
- If your dataset is very large and you hit memory limits on Streamlit Cloud, consider exporting a **trimmed CSV** with only the needed columns:
  - Size, Rental Length, Client Type, Zip, Zone, Category, Pricing Type, Weight Allowance in Tons, Client Cost, Cost per Day Over, Delivery Fee, Cost per Ton Over.
