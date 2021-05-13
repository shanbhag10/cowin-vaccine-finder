from lambda_helpers.dynamo_helper import *
from lambda_helpers.email_helper import *
from lambda_helpers.cowin_helper import *
from lambda_helpers.googlemaps_helper import *
from lambda_helpers.util_helper import *
import boto3


def notify_users(vaccine_info, alerts, table):
	for alert in alerts:
		vaccine_centers = vaccine_info[alert['district']]

		nearby_centers = find_nearby_slots(vaccine_centers, alert)
		print('Number of nearby centers : ' + str(len(nearby_centers)))

		filtered_nearby_centers = filter_old_sessions(nearby_centers, alert)
		print('Number of filtered nearby centers : ' + str(len(nearby_centers)))

		if len(nearby_centers) > 0:
			send_email(alert, filtered_nearby_centers)
			update_sessions_in_db(nearby_centers, alert, table)


def run_lambda():
	dynamodb = boto3.resource('dynamodb')
		
	table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE'))

	alerts = get_alerts_from_db(table)
	district_ids = get_distinct_district_ids(alerts)
	vaccine_info = get_total_vaccine_info(district_ids)
	notify_users(vaccine_info, alerts, table)