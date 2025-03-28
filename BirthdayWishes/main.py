from datetime import datetime
import pandas as pd
import random
import smtplib

# Email Credentials
MY_EMAIL = "prem4th11@gmail.com"
MY_PASSWORD = "olsq upfn vrvh palx"

# Get today's date
today = datetime.now()
today_tuple = (today.month, today.day)

# Read CSV and create a dictionary
data = pd.read_csv("birthdays.csv")
birthdays_dict = {(row["month"], row["day"]): row for _, row in data.iterrows()}

# Check if today matches any birthdays
if today_tuple in birthdays_dict:
    birthday_people = [row for key, row in birthdays_dict.items() if key == today_tuple]

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)

        for person in birthday_people:
            file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
            with open(file_path) as letter_file:
                contents = letter_file.read().replace("[NAME]", person["name"])

            try:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=person["email"],
                    msg=f"Subject:Happy Birthday!\n\n{contents} \n\n\n Please do not reply, this is an automated mail"
                )
                print(f"Success! Birthday email sent to {person['email']}")
            except Exception as e:
                print(f"Failed to send email to {person['email']}: {e}")

