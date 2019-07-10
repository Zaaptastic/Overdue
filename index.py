import boto3
import os

sns = boto3.client('sns')

def publish_message_to_sns(message):
	response = sns.publish(
		TopicArn=os.environ['SNS_ARN'], 
		Message=message,
		Subject="Reminder")
	
	return response
	
def handler(event, context):
	print("Publishing to ARN: " + os.environ['SNS_ARN'])
	publish_message_to_sns("test from python")
	return "done!"