"""
This Expert Advisor (EA) uses a Moving Averages strategy

This strategy makes trading decisions based on the
crossings of moving averages.

"If ma_1 crosses above ma_2 you will receive a buy signal (Vice Versa)"

Trading signals can be sent to an Email address as Text and Graph
"""
# Importing libraries
import datetime as dt
import mimetypes
import time

import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

# Graph theme
plt.style.use("grayscale")

# Moving averages
def moving_averages():
    ma_1 = 38
    ma_2 = 50
    print("This strategy will use the following Moving Averages:\n",
         ma_1, '&',  ma_2, "\n")

    return ma_1, ma_2

# Starting programme
ma_1, ma_2 = moving_averages()

# Data timeline
start = dt.datetime.now() - dt.timedelta(days=10)
end = dt.datetime.now()

# SPY Data Download
data = yf.download('USDJPY=X', start=start, end=end, interval='5m')

# SMA Calculation
data[f"SMA_{ma_1}"] = data['Adj Close'].rolling(window=ma_1).mean()
data[f"SMA_{ma_2}"] = data['Adj Close'].rolling(window=ma_2).mean()
data = data.iloc[max(ma_1, ma_2)-1:]
print(data.tail)

# Trading Signals
buy = []
sell = []
buy_signals = []
sell_signals = []
trigger = 0

for x in range(len(data)):
    if data[f"SMA_{ma_1}"].iloc[x] > data[f"SMA_{ma_2}"].iloc[x] and trigger != 1:
        buy.append(data['Adj Close'].iloc[x])
        sell.append(float('nan'))
        buy_signals.append(f"Buy signal at {data.index[x]}: Price - {round(data['Adj Close'].iloc[x], 2)}")
        trigger = 1

    elif data[f"SMA_{ma_1}"].iloc[x] < data[f"SMA_{ma_2}"].iloc[x] and trigger != -1:
        buy.append(float('nan'))
        sell.append(data['Adj Close'].iloc[x])
        sell_signals.append(f"Sell signal at {data.index[x]}: Price - {round(data['Adj Close'].iloc[x], 2)}")
        trigger = -1
    else:
        buy.append(float('nan'))
        sell.append(float('nan'))

# Sending Signals (Automate this)
buy_notification = '\n'.join(buy_signals)
sell_notification = '\n'.join(sell_signals)
print(buy_notification)
print(sell_notification)
print('Close chart to send signals via email') # add in auto chart close system

# Plotting Data
data['Buy Signals'] = buy
data['Sell Signals'] = sell
plt.plot(data['Adj Close'], label='SPY', color='blue')
plt.plot(data[f"SMA_{ma_1}"], label=f"SMA_{ma_1}", color='orange', linestyle='--')
plt.plot(data[f"SMA_{ma_2}"], label=f"SMA_{ma_2}", color='red', linestyle='--')
plt.scatter(data.index, data["Buy Signals"], label="Buy Signal", marker="^", color="#008000", lw=3)
plt.scatter(data.index, data["Sell Signals"], label="Sell Signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
# Saving Chart file
plot_filename = 'spy_trading_signals.png'
plt.savefig(plot_filename)
# Auto chart close
plt.show(block=False)
time.sleep(1)
plt.close()

# Email System
from email.message import EmailMessage
import smtplib
import ssl
password = 'uxso aftj hdoc yerz'

email_sender = 'hassan.hussain0q@gmail.com'
email_password = password               # Password: uxso aftj hdoc yerz
email_reciever = 'hussain997x@gmail.com'

subject = 'Trading signals for SPY (S&P500 Index)'
buy_subheading = 'Buy Signals'
sell_subheading = 'Sell Signals'

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciever
em['Subject'] = subject
em.set_content(f"{buy_subheading}\n{buy_notification}\n\n{sell_subheading}\n{sell_notification}")

# File attachment
ctype, encoding = mimetypes.guess_type(plot_filename)
if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)
with open(plot_filename, 'rb') as fp:
    em.add_attachment(fp.read(),maintype=maintype, subtype=subtype, filename=plot_filename)


context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())
        print('Email sent succesfully!')
except Exception as e:
    print(f"Error sending email {e}")