import streamlit as st
import pandas as pd
import random
import time

st.title("One-Page Trading App (Testing)")

# Initialize session state
if 'df' not in st.session_state:
    data = {
        "Scrip Name": ["TCS", "INFY", "HDFC", "AXISBANK", "HUL", "ITC", "TATASTEEL"],
        "CMP": [random.uniform(1000, 4000) for _ in range(7)],  # Random initial CMP
        "Limit Price": [0.0] * 7,
        "Stop Loss": [0.0] * 7,
        "Target": [0.0] * 7,
        "Qty": [0] * 7,
        "Action": ["Buy"] * 7,
        "Order Status": [""] * 7,
    }
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# Simulate live prices (random fluctuations)
if st.button("Simulate Live Prices"):
    for i in range(len(df)):
        df.loc[i, "CMP"] += random.uniform(-10, 10)  # Simulate price fluctuations
        if df.loc[i, "CMP"] < 0:
            df.loc[i, "CMP"] = 0 #Ensure that the price does not go below 0.
    st.session_state.df = df

# Allow users to input data directly in the table
edited_df = st.data_editor(df, num_rows="dynamic")

# Update session state with edited data
st.session_state.df = edited_df

# Add scrip name
new_scrip = st.text_input("Add New Scrip")
if st.button("Add Scrip"):
    if new_scrip:
        new_row = {
            "Scrip Name": new_scrip,
            "CMP": random.uniform(1000, 4000), #Random initial CMP
            "Limit Price": 0.0,
            "Stop Loss": 0.0,
            "Target": 0.0,
            "Qty": 0,
            "Action": "Buy",
            "Order Status": "",
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

# Simulate order placement, execution, and closure
if st.button("Place Orders"):
    for i in range(len(df)):
        if df.loc[i, "Order Status"] == "":
            df.loc[i, "Order Status"] = "Placed"
            st.write(f"Order placed for {df.loc[i, 'Scrip Name']}")

    for i in range(len(df)
        if df.loc[i, "Order Status"] == "Placed":
            if df.loc[i, "CMP"] >= df.loc[i, "Limit Price"]:
                df.loc[i, "Order Status"] = "Executed"
                st.write(f"Order executed for {df.loc[i, 'Scrip Name']}")
            if df.loc[i, "Order Status"] == "Executed":
                if df.loc[i, "CMP"] <= df.loc[i, "Stop Loss"]:
                    df.loc[i, "Order Status"] = "Closed (Stop Loss)"
                    st.write(f"Order closed for {df.loc[i, 'Scrip Name']} (Stop Loss)")
                elif df.loc[i, "CMP"] >= df.loc[i, "Target"]:
                    df.loc[i, "Order Status"] = "Closed (Target)"
                    st.write(f"Order closed for {df.loc[i, 'Scrip Name']} (Target)")
    st.session_state.df = df
