import uuid
import boto3
import datetime
import os
from botocore.exceptions import ClientError

class Alert:
	def __init__(self, name, email, address, pin, distance, district):
		self.id = str(uuid.uuid4())
		self.name = name
		self.email = email
		self.address = address
		self.pin = pin
		self.distance = distance
		self.district = district

	def to_string(self):
		return self.__dict__

	def save_alert(self):
		dynamodb = boto3.resource('dynamodb', 'ap-south-1', 
			aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
		
		table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE'))

		response = {}
		try:
			response = table.get_item(Key={'email': self.email})
		except ClientError as e:
			print(e.response['Error']['Message'])

		if 'Item' in response:
			return (400, "An alert already exists with the provided email. Please try a different email")

		item = {
			"id":self.id,
			"name":self.name,
			"email":self.email,
			"address":self.address,
			"pin":self.pin,
			"distance":self.distance,
			"district":self.district,
			"created_at":str(datetime.datetime.now())
		}

		table.put_item(Item=item)

		return (201, "Successfully created alert. We will send you an email when a slot is available. Thank you.")