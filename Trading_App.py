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

# Function to update CMP values
def update_cmp():
    for i in range(len(st.session_state.df)):
        if time.time() % 10 < 5:
            st.session_state.df.loc[i, "CMP"] += random.uniform(-10, 10)
            if st.session_state.df.loc[i, "CMP"] < 0:
                st.session_state.df.loc[i, "CMP"] = 0

# Function to process orders
def process_orders():
    for i in range(len(st.session_state.df)):
        if st.session_state.df.loc[i, "Action"] == "Buy" and st.session_state.df.loc[i, "Order Status"] == "":
            st.session_state.df.loc[i, "Order Status"] = "Placed"
            st.write(f"Order placed for {st.session_state.df.loc[i, 'Scrip Name']}")

        if st.session_state.df.loc[i, "Order Status"] == "Placed":
            if st.session_state.df.loc[i, "CMP"] >= st.session_state.df.loc[i, "Limit Price"]:
                st.session_state.df.loc[i, "Order Status"] = "Executed"
                st.write(f"Order executed for {st.session_state.df.loc[i, 'Scrip Name']}")

        if st.session_state.df.loc[i, "Order Status"] == "Executed":
            if st.session_state.df.loc[i, "CMP"] <= st.session_state.df.loc[i, "Stop Loss"]:
                st.session_state.df.loc[i, "Order Status"] = "Closed (Stop Loss)"
                st.session_state.df.loc[i, "Profit/Loss"] = (st.session_state.df.loc[i, "Limit Price"] - st.session_state.df.loc[i, "Stop Loss"]) * st.session_state.df.loc[i, "Qty"]
                st.write(f"Order closed for {st.session_state.df.loc[i, 'Scrip Name']} (Stop Loss)")
                st.write(f"Loss: {st.session_state.df.loc[i, 'Profit/Loss']} Rupees")
            elif st.session_state.df.loc[i, "CMP"] >= st.session_state.df.loc[i, "Target"]:
                st.session_state.df.loc[i, "Order Status"] = "Closed (Target)"
                st.session_state.df.loc[i, "Profit/Loss"] = (st.session_state.df.loc[i, "Target"] - st.session_state.df.loc[i, "Limit Price"]) * st.session_state.df.loc[i, "Qty"]
                st.write(f"Order closed for {st.session_state.df.loc[i, 'Scrip Name']} (Target)")
                st.write(f"Profit: {st.session_state.df.loc[i, 'Profit/Loss']} Rupees")

# Main loop
while True:
    # Display editable dataframe
    edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", key="data_editor")
    st.session_state.df = edited_df

    update_cmp()
    process_orders()

    st.dataframe(st.session_state.df)
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
            "Order Status": "",
            "Profit/Loss": 0.0,
        }
        st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)

# Sorting
sort_order = st.radio("Sort Scrip Names", ["Ascending", "Descending"])
if sort_order == "Ascending":
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name")
else:
    st.session_state.df = st.session_state.df.sort_values(by="Scrip Name", ascending=False)

st.dataframe(st.session_state.df)
