"""
Trading Strategy: Moving Averages
This strategy involves making trading decisions based on the crossings
of moving averages. 'If ma_1 crosses above ma_2 you get a buy signal,
and vice versa.' Stock data is used from the yFinance API and,
and the data is plotted using Matplotlib.
"""
"""
Trading Signals can be sent from and to an email address
"""

"""Importing Libraries"""
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
plt.style.use("dark_background")  # Graph Theme
pd.options.mode.chained_assignment = None  # Prevent Warnings from Being Displayed in Output

"""User Inputs"""
def inputs():
    ma_1 = None
    while ma_1 is None:
        try:
            ma_1 = int(input("Enter Primary Moving Average between 10 - 200: "))
            if ma_1 == 10 or ma_1 == 200 or (10 < ma_1 < 200):
                print("\033[1;32mPrimary Moving Average Conformed\033[m")
            else:
                print("\033[1;31mInvalid input. Please enter a valid value.\033[m")
                ma_1 = None  # Reset ma_1 to continue the loop
        except ValueError:
            print("\033[1;31mInvalid input. Please enter a valid value.\033[m")
    ma_2 = None
    while ma_2 is None:
        try:
            ma_2 = int(input("Enter Secondary Moving Average between 10 - 200: "))
            if ma_2 == 10 or ma_2 == 200 or (10 < ma_2 < 200) and ma_2 != ma_1:
                print("\033[1;32mSecondary Moving Average Conformed\033[m")
            else:
                print("\033[1;31mInvalid input. Please enter a valid value.\033[m")
                ma_2 = None  # Reset ma_2 to continue the loop
        except ValueError:
            print("\033[1;31mInvalid input. Please enter a valid value.\033[m")
    return ma_1, ma_2

"""Starting Programme"""
ma_1, ma_2 = inputs()

"""Stock Time Line"""
start = dt.datetime.now() - dt.timedelta(365 * 5)
end = dt.datetime.now()

"""Data Input & Download"""
data_request = None
while not data_request:
    data_request = input("Stock/ETF: ").upper()
    if not data_request:
        print("\033[1;31mInvalid input. Please enter a valid value.\033[m")
data = yf.download(data_request, start, end)
data[f"SMA_{ma_1}"] = data["Adj Close"].rolling(window=ma_1).mean()
data[f"SMA_{ma_2}"] = data["Adj Close"].rolling(window=ma_2).mean()

data = data.iloc[ma_2:]

"""Trading Signal System"""
buy = []
sell = []
buy_signals = []
sell_signals = []
trigger = 0  # Identify Changes

for x in range(len(data)):

    if data[f"SMA_{ma_1}"].iloc[x] > data[f"SMA_{ma_2}"].iloc[x] and trigger != 1:
        buy.append(data["Adj Close"].iloc[x])
        sell.append(float('nan'))
        buy_signals.append(f"Buy Signal at {data.index[x]}: Price - {round(data['Adj Close'].iloc[x], 2)}")
        trigger = 1
    elif data[f"SMA_{ma_1}"].iloc[x] < data[f"SMA_{ma_2}"].iloc[x] and trigger != -1:
        buy.append(float('nan'))
        sell.append(data["Adj Close"].iloc[x])
        sell_signals.append(f"Sell Signal at {data.index[x]}: Price - {round(data['Adj Close'].iloc[x],2)}")
        trigger = -1
    else:
        buy.append(float('nan'))
        sell.append((float('nan')))

buy_noti = "\n".join(buy_signals)
sell_noti = "\n".join(sell_signals)

print(buy_noti)
print(sell_noti)
print("\033[1;31mClose Pyplot Chart to Send Signals to Email!.\033[m")

"""SENDING EMAIL NOTIFICATIONS"""   # NOTE: Email will be sent once you close pyplot chart
from email.message import EmailMessage
import smtplib
import ssl

passwrd = '*ENTER PASSWORD'
email_sender = 'ENTER SENDER EMAIL'
email_pass = passwrd
email_reciever = 'ENTER RECIEVERS EMAIL'
subject = f"Trading Signals for {data_request}"
buy_subheading = "Buy Signals:"
sell_subheading = "Sell Signals:"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciever
em['Subject'] = subject
em.set_content(f"{buy_subheading}\n{buy_noti}\n\n{sell_subheading}\n{sell_noti}")

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_pass)
    smtp.sendmail(email_sender, email_reciever, em.as_string())

"""Plotting Data"""
data["Buy Signals"] = buy
data["sell Signals"] = sell
plt.plot(data["Adj Close"], label=data_request, color="blue")
plt.plot(data[f"SMA_{ma_1}"], label=f"SMA_{ma_1}", color="orange", linestyle="--")
plt.plot(data[f"SMA_{ma_2}"], label=f"SMA_{ma_2}", color="red", linestyle="--")
plt.scatter(data.index, data["Buy Signals"], label="Buy Signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data["sell Signals"], label="Sell Signal", marker="v", color="#00ff00", lw=3)
plt.legend(loc="upper left")
plt.show()
