import os
import urllib3
import json

def find_nearby_slots(vaccine_centers, alert):
	destination_sets = []
	count = 1

	destinations = ""
	for center in vaccine_centers:
		if count % 25 == 0:
			destinations += center['address'] + " " + str(center['pincode'])
			destination_sets.append(destinations)
			destinations = ""
		else:
			destinations += center['address'] + " " + str(center['pincode']) + "|"
		count+=1
		
	if destinations != "":
		destination_sets.append(destinations[:-1])

	distance_info = []
	for destinations in destination_sets:
		distance_info.extend(get_distance_info(destinations, alert))

	if len(distance_info) != len(vaccine_centers):
		print("distance_info length : "+str(len(distance_info)))
		print("vaccine_centers length : "+str(len(vaccine_centers)))
		return []

	nearby_centers = []
	for i in range(len(vaccine_centers)):
		if distance_info[i]['status'] == "OK":
			distance = distance_info[i]['distance']['value'] / 1000
			if distance <= float(alert['distance']):
				nearby_centers.append(vaccine_centers[i])

	return nearby_centers


def get_distance_info(destinations, alert):
	origin = alert['address'] + " " + alert['pin']

	command = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origin.replace(" ", "+").replace(",", "") + "&destinations=" + destinations.replace(" ", "+").replace(",", "") + "&key=" + os.environ.get('GOOGLE_MAPS_API_KEY')
	
	http = urllib3.PoolManager()
	response = http.request('GET', command)

	if response.status != 200:
		print("error from gmaps: " +str(response.status))
		return []

	return json.loads(response.data)['rows'][0]['elements']