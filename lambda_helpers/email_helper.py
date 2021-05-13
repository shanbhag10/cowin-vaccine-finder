import boto3
from botocore.exceptions import ClientError


def build_email_content(nearby_centers):
	html_body = """
	<html>
	<head>
	<style>
	table {
		border: 1px solid black;
		border-collapse: collapse;
		text-align: center;
		font-size: 90%;
		width: 100%;
	}

	th {
		padding-top: 12px;
		padding-bottom: 12px;
		background-color: #006bb3;
		color: white;
		font-size: 110%;
	}

	#centers tr {
		border: 2px solid #006bb3;
	}

	#slots td {
		border: 0px solid #ccc;
	}

	#sessions td {
		font-size: 85%;
	}

	#slots tr, th, td {
		border: 1px solid #ccc;
	}

	.center_info {
		width: 33%;
	}
	</style>
	</head>
	<body>
	  <h1>Open Vaccine Slots Found - Book Now</h1>
	  <table id="centers">
	    <tr>
		  <th>Center Info</th>
   	      <th>Available Slots</th>
	  	</tr>
	  """

	for center_info in nearby_centers:	
		html_body += "<tr>"
		html_body += "<td class='center_info'>" + center_info['name'] + "<br />" + center_info['address'] + "<br />" + str(center_info['pincode']) + "</td>"
		html_body += "<td> <table id='slots'>" 

		for session in center_info['sessions']:
			html_body += "<tr>"
			html_body += "<td>" + session['date'] + "</td>"
			html_body += "<td> <table id='sessions'>" 

			for slot in session['slots']:
				html_body += "<tr><td>" + slot + "</td></tr>"
			
			html_body += "</table></td>"
			html_body += "</tr>"   

		html_body += "</table></td>"
		html_body += "</tr>"

	html_body += """</table>
		<p>To unsubscribe, please click
	    	<a href='https://aws.amazon.com/ses/'>here</a>
	    </p>
	</body>
	</html>
	"""     

	return html_body


def send_email(alert, nearby_centers):
	SENDER = "Covid Vaccine Finder <go.coronaaa.go@gmail.com>"
	
	SUBJECT = "Open Vaccine Slots Found in your Area - Book Now"
	
	BODY_TEXT = (str(nearby_centers))
	            
	BODY_HTML = build_email_content(nearby_centers)       
	
	CHARSET = "UTF-8"
	
	client = boto3.client('ses',region_name="ap-south-1")
	
	try:
	    response = client.send_email(
	        Destination={
	            'ToAddresses': [
	                alert['email'],
	            ],
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data': BODY_HTML,
	                },
	                'Text': {
	                    'Charset': CHARSET,
	                    'Data': BODY_TEXT,
	                },
	            },
	            'Subject': {
	                'Charset': CHARSET,
	                'Data': SUBJECT,
	            },
	        },
	        Source=SENDER,
	    )
	except ClientError as e:
	    print(e.response['Error']['Message'])
	else:
	    print("Email sent! Message ID:" + response['MessageId'])