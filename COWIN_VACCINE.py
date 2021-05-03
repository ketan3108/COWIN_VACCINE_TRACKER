import requests
import datetime
import json
import smtplib
POST_CODE = "123401"
age = 18
# Print details flag
print_flag = 'Y'

numdays = 20
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
for INP_DATE in date_str:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(POST_CODE, INP_DATE)
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
        # print(json.dumps(resp_json, indent = 1))
        flag = False
        if resp_json["centers"]:
            print("Available on: {}".format(INP_DATE))
            if(print_flag=='y' or print_flag=='Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age:
                            print("\t", center["name"])
                            print("\t", center["block_name"])
                            print("\t Price: ", center["fee_type"])
                            print("\t Available Capacity: ", session["available_capacity"])
                            if(session["available_capacity"]>0):
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                server.login("yOUREMAILID.COM","PWD") #logs into your email account
                                print("Login Success")#confirms that you have logged in succesfully
                                server.sendmail("SENDEREMAIL.COM","RECEIVER","Vaccine Avialable on {} at {}".format(INP_DATE,center["name"]))#send the email with your custom mesage
                                # print("Center : {}".format(center["name"]))
                                print("Email was sent") #confirms that the email was sent

                            if(session["vaccine"] != ''):
                                print("\t Vaccine: ", session["vaccine"])
                            print("\n\n")
                            
            
                
        else:
            print("No available slots on {}".format(INP_DATE))