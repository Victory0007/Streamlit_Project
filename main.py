import streamlit as st
import json
import requests

# Defined ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Load data from JSON file
with open("data.json") as file:
    data = file.read()

# Parse JSON data
try:
    json_data = json.loads(data)
except json.JSONDecodeError as e:
    st.error(f"Error loading JSON: {e}")
    st.stop()

# Fetching announcements for all tickers
all_announcements = {}
for ticker in tickers:
    if ticker in json_data and 'data' in json_data[ticker]:
        announcements = json_data[ticker]['data']
        all_announcements[ticker] = announcements
    else:
        st.warning(f"No data found for ticker: {ticker}")

# Streamlit app layout
st.title("ASX Announcements Viewer")

# Filtering by ticker symbol
selected_ticker = st.selectbox("Select a Ticker", tickers)

# Displaying announcements for the selected ticker
if selected_ticker in all_announcements:
    st.subheader(f"Recent Announcements for {selected_ticker}")
    for announcement in all_announcements[selected_ticker]:
        st.write(f"**{announcement['header']}**")
        st.write(f"Release Date: {announcement['document_release_date']}")
        st.write(f"[View Document]({announcement['url']})")
        st.write("---")
else:
    st.warning(f"No announcements available for {selected_ticker}")

# Displaying tickers with "Trading Halt" announcements
st.subheader("Tickers with 'Trading Halt' Announcements")
for ticker, announcements in all_announcements.items():
    for announcement in announcements:
        if "Trading Halt" in announcement['header']:
            st.write(f"Ticker: {ticker}")
            st.write(f"**{announcement['header']}**")
            st.write(f"Release Date: {announcement['document_release_date']}")
            st.write(f"[View Document]({announcement['url']})")
            st.write("---")


# Code I wrote to fetch the data from the api link
api_base_url = "https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"


def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements"
    try:
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Cookie': 'JSESSIONID=.node104; nlbi_2835827_2708396=hdX4cEIto1irsB9/2S5TNgAAAAAndFs7w+ilBKPt91w9epMB; visid_incap_2835827=AP+xQP+iQ1iXy8HVbLFOb6iyvWYAAAAAQUIPAAAAAACPk2er6pQsd3c6H2CNNWDr; affinity="2846651b15df7f28"; nlbi_2835827=RdNsQaQW5yLlAMx02S5TNgAAAABulA+kHWxDEDJQZBgvRJfx; TS019c39fc=01856a822a81b1e1324fd3be2854a52a4a5e6cf8dedb1d7ad737d495fc4da32682d827f24d434fa387b650059794d89bb589cc84a5; incap_ses_2222_2835827=3PuxHw892FNPx02SdCHWHlH4vWYAAAAAlR97D3Hwla6it0rK4wz9SQ=='}
        response = requests.request("GET", url, headers=headers, data=payload)

        # if the response is successful
        if response.status_code == 200:
            try:
                # parsing the JSON response
                return response.json().get('data', [])
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON. Response content:", response.text)
                return []  # Returns an empty list in case of JSON decoding error
        else:
            print(f"Request failed with status code {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
