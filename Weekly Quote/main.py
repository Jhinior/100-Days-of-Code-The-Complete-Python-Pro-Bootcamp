import smtplib
import random
import datetime as dt
import os
now = dt.datetime.now()
day_of_week = now.weekday()
if day_of_week == 0:
    my_email = os.environ["my_email"]
    password = os.environ["my_pass"]
    connection = smtplib.SMTP("smtp.gmail.com",587)
    connection.starttls()
    connection.login(user= my_email, password= password)
    with open("quotes.txt") as file:
        list = file.readlines()
        qoute = [n.strip() for n in list]
        to_send = random.choice(qoute)
    connection.sendmail(from_addr= my_email , to_addrs= my_email , msg= f"Subject: Quote of the week \n\n"
    f"{to_send}")
    connection.close()
