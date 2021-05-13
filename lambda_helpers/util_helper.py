def get_distinct_district_ids(alerts):
	district_ids = set()
	for alert in alerts:
		if alert['district'].isnumeric():
			district_ids.add(alert['district'])

	print("Districts to scan : " + str(district_ids))
	return district_ids


def filter_old_sessions(nearby_centers, alert):
	if 'sessions_alerted' not in alert.keys():
		return nearby_centers

	alerted_sessions = set(alert['sessions_alerted'].split(","))

	filtered_centers = []
	for center in nearby_centers:
		new_sessions = []
		for session in center['sessions']:
			if session['session_id'] not in alerted_sessions:
				new_sessions.append(session)

		if len(new_sessions) > 0:
			center['sessions'] = new_sessions
			filtered_centers.append(center)

	return filtered_centers