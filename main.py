import requests
from datetime import datetime
import smtplib

MY_LAT = 50.110924
MY_LNG = 8.682127

# ----------------------- OPTIONAL: SMTP SETUP -----------------------------------------#
# def send_mail():
#     my_email = "shaunsmtptest@gmail.com"
#     password = "scmdfgcxbehlqlak"
#
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(user=my_email, password=password)
#         connection.sendmail(
#                             from_addr=my_email,
#                             to_addrs="shaunsmtptest@yahoo.com",
#                             msg="Subject:Motivational Quote\n\nThe ISS is right above you, look up!"
#                             )


# ----------------------- ISS POSITION -----------------------------------------#
def is_iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_longitude = float(iss_response.json()["iss_position"]["longitude"])
    iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True


# ----------------------- SUNRISE / SUNSET AT CURRENT LOCATION -----------------------------------------#
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    data = sun_response.json()

    # .split() converts this: 2023-01-23T07:08:57+00:00 to this: 07
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


# ----------------------- OPTIONAL: SEND MAIL IF ISS IN MY SKY -----------------------------------------#
if is_iss_overhead() and is_night():
    send_mail()


