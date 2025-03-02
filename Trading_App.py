import streamlit as st
import pandas as pd
from kiteconnect import KiteConnect
import time

st.title("One-Page Trading App")

# API Key Input
api_key = st.text_input("Enter Zerodha API Key:")
api_secret = st.text_input("Enter Zerodha API Secret:", type="password")

if api_key and api_secret:
    try:
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()
        st.write(f"Login: {login_url}")
        request_token = st.text_input("Enter request token:")

        if request_token:
            data = kite.generate_session(request_token, api_secret=api_secret)
            kite.set_access_token(data["access_token"])

            st.write("Authentication successful!")

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

            # Fetch live prices (using kite object)
            for i in range(len(df)):
                try:
                    instrument_token = kite.instruments(exchange=kite.EXCHANGE_NSE, tradingsymbol=df.loc[i, "Scrip Name"])[0]['instrument_token']
                    live_price = kite.ltp([instrument_token])[str(instrument_token)]['last_price']
                    df.loc[i, "CMP"] = live_price
                except:
                    df.loc[i, "CMP"] = 0

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
                    try:
                        instrument_token = kite.instruments(exchange=kite.EXCHANGE_NSE, tradingsymbol=new_scrip)[0]['instrument_token']
                        new_cmp = kite.ltp([instrument_token])[str(instrument_token)]['last_price']
                    except:
                        new_cmp = 0
                    new_row = {
                        "Scrip Name": new_scrip,
                        "CMP": new_cmp,
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

    except Exception as e:
        st.error(f"Error: {e}")
