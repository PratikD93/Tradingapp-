import streamlit as st
import pandas as pd
import random
import time

st.title("One-Page Trading App (Detailed)")

# Initialize session state
if 'df' not in st.session_state:
    data = {
        "Scrip Name": ["TCS", "INFY", "HDFC", "AXISBANK", "HUL", "ITC", "TATASTEEL"],
        "CMP": [random.uniform(1000, 4000) for _ in range(7)],
        "Limit Price": [0.0] * 7,
        "Stop Loss": [0.0] * 7,
        "Target": [0.0] * 7,
        "Qty": [0] * 7,
        "Action": ["Buy"] * 7,
        "Order Status": [""] * 7,
        "Profit/Loss": [0.0] * 7,
    }
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# Allow users to input data directly in the table
edited_df = st.data_editor(df, num_rows="dynamic")

# Update session state with edited data
st.session_state.df = edited_df
df = st.session_state.df

# Place orders on "Buy" action
for i in range(len(df)):
    if df.loc[i, "Action"] == "Buy" and df.loc[i, "Order Status"] == "":
        df.loc[i, "Order Status"] = "Placed"
        st.write(f"Order placed for {df.loc[i, 'Scrip Name']}")

# Simulate live prices and automatic order closure
while True:
    for i in range(len(df)):
        # Generate random CMP every 10 seconds
        if time.time() % 10 < 5:  # Generate new CMP in the first 5 seconds
            df.loc[i, "CMP"] += random.uniform(-10, 10)
            if df.loc[i, "CMP"] < 0:
                df.loc[i, "CMP"] = 0

        if df.loc[i, "Order Status"] == "Placed":
            if df.loc[i, "CMP"] >= df.loc[i, "Limit Price"]:
                df.loc[i, "Order Status"] = "Executed"
                st.write(f"Order executed for {df.loc[i, 'Scrip Name']}")
        if df.loc[i, "Order Status"] == "Executed":
            if df.loc[i, "CMP"] <= df.loc[i, "Stop Loss"]:
                df.loc[i, "Order Status"] = "Closed (Stop Loss)"
                df.loc[i, "Profit/Loss"] = (df.loc[i, "Limit Price"] - df.loc[i, "Stop Loss"]) * df.loc[i, "Qty"]
                st.write(f"Order closed for {df.loc[i, 'Scrip Name']} (Stop Loss)")
                st.write(f"Loss: {df.loc[i, 'Profit/Loss']} Rupees")
            elif df.loc[i, "CMP"] >= df.loc[i, "Target"]:
                df.loc[i, "Order Status"] = "Closed (Target)"
                df.loc[i, "Profit/Loss"] = (df.loc[i, "Target"] - df.loc[i, "Limit Price"]) * df.loc[i, "Qty"]
                st.write(f"Order closed for {df.loc[i, 'Scrip Name']} (Target)")
                st.write(f"Profit: {df.loc[i, 'Profit/Loss']} Rupees")
    st.session_state.df = df
    st.dataframe(df)
    time.sleep(5)  # Check every 5 seconds

# Add scrip name
new_scrip = st.text_input("Add New Scrip")
if st.button("Add Scrip"):
    if new_scrip:
        new_row = {
            "Scrip Name": new_scrip,
            "CMP": random.uniform(1000, 4000),
            "Limit Price": 0.0,
            "Stop Loss": 0.0,
            "Target": 0.0,
            "Qty": 0,
            "Action": "Buy",
            "Order Status": "",
            "Profit/Loss": 0.0,
        }
        st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
        df = st.session_state.df

# Sorting
sort_order = st.radio("Sort Scrip Names", ["Ascending", "Descending"])
if sort_order == "Ascending":
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name")
else:
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name", ascending=False)

df = st.session_state.df

# Display the DataFrame
st.dataframe(df)
