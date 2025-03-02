import streamlit as st
import pandas as pd
import requests
import datetime

st.title("One-Page Trading App")

# Function to fetch closing price for a specific date
def get_specific_date_close(symbol, target_date):
    date_string = target_date.strftime("%Y-%m-%d")

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?region=IN&lang=en-IN&includePrePost=false&interval=1d&range=365d"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        timestamps = data['chart']['result'][0]['timestamp']
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']

        for i, timestamp in enumerate(timestamps):
            date = datetime.datetime.fromtimestamp(timestamp).date()
            if date == target_date.date():
                return closes[i]

        return 0.0  # Return 0.0 if date not found
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching price for {symbol}: {e}")
        return 0.0
    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error parsing data for {symbol}: {e}")
        return 0.0

# Initialize session state
if 'df' not in st.session_state:
    data = {
        "Scrip Name": ["TCS", "INFY", "HDFC", "AXISBANK", "HUL", "ITC", "TATASTEEL"],
        "CMP": [0.0] * 7,
        "Limit Price": [0.0] * 7,
        "Stop Loss": [0.0] * 7,
        "Target": [0.0] * 7,
        "Qty": [0] * 7,
        "Action": ["Buy"] * 7,
        "Order Status": [""] * 7,
    }
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# Fetch closing prices for the specific date
target_date = datetime.datetime(2024, 2, 28) #Here is the changed date.
for i in range(len(df)):
    df.loc[i, "CMP"] = get_specific_date_close(df.loc[i, "Scrip Name"], target_date)

# Allow users to input data
for i in range(len(df)):
    df.loc[i, "Limit Price"] = st.number_input(f"Limit Price for {df.loc[i, 'Scrip Name']}", value=0.0, key=f"limit_{i}")
    df.loc[i, "Stop Loss"] = st.number_input(f"Stop Loss for {df.loc[i, 'Scrip Name']}", value=0.0, key=f"sl_{i}")
    df.loc[i, "Target"] = st.number_input(f"Target for {df.loc[i, 'Scrip Name']}", value=0.0, key=f"target_{i}")
    df.loc[i, "Qty"] = st.number_input(f"Qty for {df.loc[i, 'Scrip Name']}", value=0, key=f"qty_{i}")

# Add scrip name
new_scrip = st.text_input("Add New Scrip")
if st.button("Add Scrip"):
    if new_scrip:
        new_row = {
            "Scrip Name": new_scrip,
            "CMP": get_specific_date_close(new_scrip, target_date),
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

    for i in range(len(df)):
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
