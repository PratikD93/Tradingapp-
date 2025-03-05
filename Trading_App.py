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
        "Profit/Loss": [0.0] * 7,
        "Buy Price": [0.0] * 7,
        "Sell Price": [0.0] * 7,
    }
    st.session_state.df = pd.DataFrame(data)

# Display editable dataframe initially
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", key="data_editor")

# Update session state ONLY when the DataFrame is changed
if not edited_df.equals(st.session_state.df):
    st.session_state.df = edited_df

# Create a placeholder for the dataframe
dataframe_placeholder = st.empty()

# Function to update CMP values
def update_cmp():
    for i in range(len(st.session_state.df)):
        if time.time() % 10 < 5:
            st.session_state.df.loc[i, "CMP"] += random.uniform(-10, 10)
            if st.session_state.df.loc[i, "CMP"] < 0:
                st.session_state.df.loc[i, "CMP"] = 0

# Function to process orders
def process_orders():
    if 'order_placed' not in st.session_state:
        st.session_state.order_placed = {}

    for i in range(len(st.session_state.df)):
        if st.session_state.df.loc[i, "Action"] == "Buy" and i not in st.session_state.order_placed:
            st.session_state.order_placed[i] = "Placed"
            st.session_state.df.loc[i, "Buy Price"] = st.session_state.df.loc[i, "Limit Price"]

        if i in st.session_state.order_placed and st.session_state.order_placed[i] == "Placed":
            if st.session_state.df.loc[i, "CMP"] >= st.session_state.df.loc[i, "Limit Price"]:
                st.session_state.order_placed[i] = "Executed"

        if i in st.session_state.order_placed and st.session_state.order_placed[i] == "Executed":
            if st.session_state.df.loc[i, "CMP"] <= st.session_state.df.loc[i, "Stop Loss"]:
                del st.session_state.order_placed[i]
                st.session_state.df.loc[i, "Profit/Loss"] = (st.session_state.df.loc[i, "Limit Price"] - st.session_state.df.loc[i, "Stop Loss"]) * st.session_state.df.loc[i, "Qty"]
                st.session_state.df.loc[i, "Sell Price"] = st.session_state.df.loc[i, "Stop Loss"]
            elif st.session_state.df.loc[i, "CMP"] >= st.session_state.df.loc[i, "Target"]:
                del st.session_state.order_placed[i]
                st.session_state.df.loc[i, "Profit/Loss"] = (st.session_state.df.loc[i, "Target"] - st.session_state.df.loc[i, "Limit Price"]) * st.session_state.df.loc[i, "Qty"]
                st.session_state.df.loc[i, "Sell Price"] = st.session_state.df.loc[i, "Target"]

# Main loop
while True:
    update_cmp()
    process_orders()

    dataframe_placeholder.dataframe(st.session_state.df)

    time.sleep(5)

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
            "Profit/Loss": 0.0,
            "Buy Price": 0.0,
            "Sell Price": 0.0,
        }
        st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)

# Sorting
sort_order = st.radio("Sort Scrip Names", ["Ascending", "Descending"])
if sort_order == "Ascending":
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name")
else:
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name", ascending=False)

st.dataframe(st.session_state.df)
