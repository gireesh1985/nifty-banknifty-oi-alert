
import requests
import pandas as pd
from datetime import datetime

BOT_TOKEN = "7005370202:AAHEy3Oixk3nYCARxr8rUlaTN6LCUHeEDlI"
CHAT_ID = "537459100"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def get_option_chain(symbol):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    with requests.Session() as s:
        try:
            s.get("https://www.nseindia.com", headers=headers, timeout=5)
            r = s.get(url, headers=headers, timeout=5)
            return r.json()
        except Exception as e:
            print(f"Failed to fetch data for {symbol}:", e)
            return None

def extract_atm_strike(spot_price, strike_list):
    return min(strike_list, key=lambda x: abs(x - spot_price))

def analyze_oi(symbol):
    data = get_option_chain(symbol)
    if not data:
        return

    records = data["records"]["data"]
    underlying = data["records"]["underlyingValue"]
    strikes = data["records"]["strikePrices"]
    atm = extract_atm_strike(underlying, strikes)
    watch_range = [atm - 200, atm - 100, atm, atm + 100, atm + 200]

    alerts = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for r in records:
        strike = r.get("strikePrice")
        if strike in watch_range:
            ce_oi_pct = r.get("CE", {}).get("pchangeinOpenInterest", 0)
            pe_oi_pct = r.get("PE", {}).get("pchangeinOpenInterest", 0)

            if ce_oi_pct >= 30:
                alerts.append(f"🔴 {symbol} CE OI Surge\nStrike: {strike}\nOI Change: +{ce_oi_pct:.1f}% 📉")
            if pe_oi_pct >= 30:
                alerts.append(f"🟢 {symbol} PE OI Surge\nStrike: {strike}\nOI Change: +{pe_oi_pct:.1f}% 📈")

    if alerts:
        full_msg = f"📊 {symbol} OI ALERT - {now}\n\n" + "\n\n".join(alerts)
        send_alert(full_msg)
        print(full_msg)
    else:
        print(f"[{now}] No significant OI change for {symbol}.")

def main():
    analyze_oi("NIFTY")
    analyze_oi("BANKNIFTY")

if __name__ == "__main__":
    main()
