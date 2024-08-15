import streamlit as st
import requests

# Defined ticker symbols and the base API URL
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']
api_base_url = "https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"


# Created a function to fetch announcements for a ticker

def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements"
    try:
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Cookie': 'JSESSIONID=.node104; nlbi_2835827_2708396=hdX4cEIto1irsB9/2S5TNgAAAAAndFs7w+ilBKPt91w9epMB; visid_incap_2835827=AP+xQP+iQ1iXy8HVbLFOb6iyvWYAAAAAQUIPAAAAAACPk2er6pQsd3c6H2CNNWDr; affinity="2846651b15df7f28"; nlbi_2835827=RdNsQaQW5yLlAMx02S5TNgAAAABulA+kHWxDEDJQZBgvRJfx; TS019c39fc=01856a822ade6097b19a6fdcdecdb0d257cc4aef15b2ad8282e88bd87962fad249835bed134dc7a6e7567c8a50952ee77f1c7f0653; incap_ses_2222_2835827=VVfxNNgaqQBXccyRdCHWHi7TvWYAAAAA327L0PimO5SuRSe5JWSu+A=='}
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


# Fetching announcements for all tickers
all_announcements = {}
for ticker in tickers:
    announcements = fetch_announcements(ticker)
    all_announcements[ticker] = announcements

# Streamlit app layout
st.title("ASX Announcements Viewer")

# Filtering by ticker symbol
selected_ticker = st.selectbox("Select a Ticker", tickers)

# Displaying announcements for the selected ticker
if selected_ticker:
    st.subheader(f"Recent Announcements for {selected_ticker}")
    for announcement in all_announcements[selected_ticker]:
        st.write(f"**{announcement['header']}**")
        st.write(f"Release Date: {announcement['document_release_date']}")
        st.write(f"[View Document]({announcement['url']})")
        st.write("---")

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
