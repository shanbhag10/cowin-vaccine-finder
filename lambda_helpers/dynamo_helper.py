import datetime

def get_alerts_from_db(table):
	response = table.scan()
	data = response['Items']

	while 'LastEvaluatedKey' in response:
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data.extend(response['Items'])

	print("Number of alerts : " + str(len(data)))
	return data


def update_sessions_in_db(nearby_centers, alert, table):
	session_ids = []
	for center in nearby_centers:
		for session in center['sessions']:
			session_ids.append(session['session_id'])

	session_ids_str = ','.join(session_ids)

	response = table.update_item(
		Key={'email': alert['email']},
		UpdateExpression="set sessions_alerted=:s, email_sent_at=:e",
		ExpressionAttributeValues={
			':s': session_ids_str,
			':e': str(datetime.datetime.now())
		},
		ReturnValues="UPDATED_NEW"
	)

	return response