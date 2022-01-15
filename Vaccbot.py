import requests
from datetime import datetime
import time
import schedule


base_cowin_url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=375&date=18-09-2021"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
solapur_district_id="375"
api_url_telegram = "https://api.telegram.org/bot2038161679:AAEROAYjjFTKILwZBqzj-Gj65It7-c6Svwc/sendMessage?chat_id=__groupid__&text="
group_id = "-1001553783342"
 



def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&data={}".format(district_id, today_date)
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url,headers=headers)
    extract_availability_data(response)
    print(response.text)

def extract_availability_data(response):
  response_json = response.json()
  for center in response_json["centers"]:
    for session in center["sessions"]:
      if  session["vaccine"]=="COVAXIN" and center["fee_type"]=="Free" and  center["pincode"] <= 413009 and session["available_capacity_dose2"] > 1 and session["min_age_limit"] == 18:
         message = "Vaccine: {} \nCenter Name: {} \nPincode: {} \nCost: {} \nDose 2 Slots:{} \nAge Limit: {} \nDate: {} \nSITE :https://selfregistration.cowin.gov.in/".format(
          session["vaccine"],center["name"],center["pincode"], 
          center["fee_type"] , 
          session["available_capacity_dose2"],
          session["min_age_limit"],
          session["date"]

          )
         
         send_message_telegram(message)

def send_message_telegram(message):
  final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
  final_telegram_url = final_telegram_url + message
  response = requests.get(final_telegram_url)  
  print(response)
           


if __name__ == "__main__":
    schedule.every(15).seconds.do(lambda: (fetch_data_from_cowin(solapur_district_id)))
    while True:
      schedule.run_pending()
      time.sleep(2)
    
