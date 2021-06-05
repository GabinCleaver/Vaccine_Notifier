import requests
import time
from datetime import datetime, timedelta

age = int(input("Entrez l'âge de la personne: "))
pincodes = ['560076']
num_days = int(input("Entrez le nombre de jours: "))

today = datetime.today()
further_days = [today + timedelta(days=i) for i in range(num_days)]
dates = [i.strftime("%d-%m-%Y") for i in further_days]

while True:
    cnt = 0
    for pincode in pincodes:
        for date in dates:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, date)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
                }
            result = requests.get(url, headers = headers)
            if result.ok:
              response_json = result.json()
              flag = False
              if response_json['centers']:
                for center in response_json['centers']:
                  for session in center['sessions']:
                    if session['min_age_limit']<=age and session['available_capacity']>0:
                      print('\nPincode: ' + pincode)
                      print('\nDate de disponibilité: ' + date)
                      print("\nAddresse: "+center['address'])
                      print("\nCentre: "+center['name'])
                      print("\nNom du bloc: "+center['block_name'])
                      print("\nPrix: "+center['fee_type'])
                      print("\nCapacité disponible (Dose 1): "+str(session['available_capacity_dose1']))
                      print("\nCapacité disponible (Dose 2): "+str(session['available_capacity_dose2']))
                      print("\nType de vaccin: "+session['vaccine'])
                      cnt+=1
            else:
              print("\nProblème avec l'API. Pas de réponse.")
    if cnt==0:
      print("\nPas de créneaux pour les vaccins disponibles.")
    else:
      print("\nVaccin trouvé ! Veuillez trouver les détails ci-dessus!")
      print("\nSe connecter à https://www.cowin.gov.in/home -> S'identifier -> Prenez rendez-vous pour le vaccin en utilisant les détails.")

    print("\n==================================\n")

    delay = datetime.now()+timedelta(minutes=2)
    while datetime.now() < delay:
      time.sleep(10)