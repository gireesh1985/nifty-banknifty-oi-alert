def fetch_iv_rv_data(symbol="BANKNIFTY"):
    try:
        log(f"🔄 Fetching IV-RV data for {symbol}...")
        session = create_session_with_retries()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.nseindia.com',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }

        if not fetch_nse_cookies(session, headers):
            error_msg = "Failed to initialize session cookies"
            log(f"❌ {error_msg}")
            asyncio.run(send_telegram_alert(error_msg, is_error=True))
            return None, None, None

        time.sleep(2)  # Increased delay to avoid rate-limiting

        oc_url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        response = session.get(oc_url, headers=headers, timeout=15)
        log(f"Option chain response: HTTP {response.status_code}, Content-Length: {len(response.content)}")
        # ... rest of the function remains the same until historical data
        time.sleep(2)  # Delay before historical data request
        historical_url = (
            f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}"
            f"&from={start_date.strftime('%d-%m-%Y')}&to={end_date.strftime('%d-%m-%Y')}"
        )
        response = session.get(historical_url, headers=headers, timeout=15)
        # ... rest of the function
    except Exception as e:
        error_msg = f"Error fetching IV/RV data: {str(e)}"
        log(f"❌ {error_msg}")
        asyncio.run(send_telegram_alert(error_msg, is_error=True))
        return None, None, None