import requests
from bs4 import BeautifulSoup
import datetime as dt
import smtplib
import os

today = dt.datetime.now()
time = today.strftime("%H:%M:%S")
PASS = os.environ["pass"]
EMAIL = os.environ["mail"]
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language" : "en-US,en;q=0.9"
}

response = requests.get(url=URL,headers=headers)
amazon = response.text

soup = BeautifulSoup(amazon,"html.parser")
price_whole = int(soup.find(name="span",class_="a-price-whole").get_text().split(".")[0])
price_fraction = int(soup.find(name="span",class_="a-price-fraction").get_text())
price = price_whole + (price_fraction/100)
repeat = True
while repeat:
    if price < 100 and time == "00:00:00":
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=EMAIL,password=PASS)
        connection.sendmail(from_addr=EMAIL,to_addrs=EMAIL,msg=f"Subject: You got a nice offer \n\n"
                                                               f"The price of the product you want is {price}$ "
                                                               f"which is a great offer for you")
        connection.close()
        repeat = False

