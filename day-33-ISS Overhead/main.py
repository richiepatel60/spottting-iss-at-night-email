import requests
from datetime import datetime
import smtplib

MY_EMAIL = "hbanner2500@gmail.com"
PASSWORD = "hulkbuster"

MY_LAT = 23.022505  # Your latitude
MY_LONG = 72.571365  # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.
def iss_is_near():
    if MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LONG - 5 < iss_longitude < MY_LONG + 5:
        return True


parameters = {
    # "lat": MY_LAT,
    # "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = int(datetime.now().hour)

# If the ISS is close to my current position and it is currently dark
if sunrise < time_now < sunset:
    pass
else:
    if iss_is_near():
        # Then send me an email to tell me to look up.
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg="Subject: Look Up👆\n\n International space station is overhead"
                                )

# following code will help to run code 24 hours every 60 secs so we can spot ISS in sky at night.
# BONUS: run the code every 60 seconds.

# import time
# time.sleep(60)
# while True:
#     if iss_is_near():
#         # Then send me an email to tell me to look up.
#         with smtplib.SMTP("smtp.gmail.com") as connection:
#             connection.starttls()
#             connection.login(user=MY_EMAIL, password=PASSWORD)
#             connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
#                                 msg="Subject: Look Up👆\n\n International space station is overhead"
#                                 )
