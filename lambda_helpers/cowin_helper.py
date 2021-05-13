import json
from datetime import datetime 
import urllib3


def get_total_vaccine_info(district_ids):
	vaccine_info = {}

	for district_id in district_ids:	
		vaccine_info[district_id] = search_slots(district_id, datetime.today().strftime('%d-%m-%Y'))

	return vaccine_info


def search_slots(district_id, today_date):
	command = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + district_id + "&date=" +today_date

	http = urllib3.PoolManager()

	response = http.request(
		'GET', 
		command, 
		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
	
	if response.status == 200:
		centers = json.loads(response.data)['centers']
		print("Number of centers for district_id : " + str(district_id) + " = " + str(len(centers)))
		return centers
		
	print('Response Status' + str(response.status))
	return {}