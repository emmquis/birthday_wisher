
import datetime as dt
import os
from random import choice
import smtplib
import pandas

MY_EMAIL = os.environ["EMAIL_VAR"]
PASSWORD = os.environ["PASS_VAR"]
SMTP_URL = os.environ["SMTP_VAR"]

# 1. Update the birthdays.csv
try:
    data = pandas.read_csv("birthdays.csv")
    birthday_dict = data.to_dict("records")
except FileNotFoundError:
    # create a CSV file
    birthday_dict = [{"name": "Test",
                      "email": "test@email.com",
                      "year": 2001,
                      "month": 1,
                      "day": 1,
                      }]
    df = pandas.DataFrame(birthday_dict)
    df.to_csv("birthdays.csv", index=0)

now = dt.datetime.now()
now_month = now.month
now_day = now.day
# print(now_month, now_day)

# 2. Check if today matches a birthday in the birthdays.csv
birthday_info = {}
for info in birthday_dict:
    if info["month"] == now_month and info["day"] == now_day:
        birthday_info["name"] = info["name"]
        birthday_info["email"] = info["email"]
        birthday_info["year"] = info["year"]
        birthday_info["month"] = info["month"]
        birthday_info["day"] = int(info["day"])

        # print(birthday_info)

        # 3. If step 2 is true, pick a random letter from letter templates
        # and replace the [NAME] with the person's actual name from birthdays.csv

        letter_list = ["letter_1", "letter_2", "letter_3"]
        birthday_letter = choice(letter_list) + ".txt"
        # print(birthday_letter)

        # 4. Send the letter generated in step 3 to that person's email address.
        with open(f"./letter_templates/{birthday_letter}") as file:
            letter = file.read()
            new_letter = letter.replace("[NAME]", birthday_info["name"])
        # print(new_letter)

        with smtplib.SMTP(SMTP_URL) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=birthday_info["email"],
                                msg=f"Subject:Happy Birthday!\n\n{new_letter}")
    # else:
    #     print("No one has a birthday today!")
