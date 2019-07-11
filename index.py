import boto3
import os
import pickle
import datetime as dt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

sns = boto3.client('sns')

def publish_message_to_sns(task_title):
	message = "You have one overdue task: " + task_title
	
	response = sns.publish(
		TopicArn=os.environ['SNS_ARN'], 
		Message=message,
		Subject=task_title)
	
	return response
	
def is_time_overdue(time_string):
	due_time = dt.datetime.strptime(time_string, '%Y-%m-%d')
	overdue_time = dt.datetime.now() + dt.timedelta(days=1)
	print("\t\tProcessing due time: " + str(due_time))
	if overdue_time > due_time:
		return True
	return False
	
def handler(event, context):
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	with open('token.pickle', 'rb') as token:
		creds = pickle.load(token)

	service = build('tasks', 'v1', credentials=creds)

	# Call the Tasks API
	results = service.tasklists().list(maxResults=10).execute()
	items = results.get('items', [])

	if not items:
		print('No task lists found.')
	else:
		print('Task lists:')
		for item in items:
			print(u'{0} ({1})'.format(item['title'], item['id']))
			
			results = service.tasks().list(tasklist=item['id']).execute()
			tasks_list = results.get('items', [])
			for task_item in tasks_list:
				print("\tProcessing task: " + task_item['title'])
				if 'due' in task_item.keys():
					if is_time_overdue(str(task_item['due']).split('T')[0]):
						print("\t\tTask is overdue, sending SNS reminder")
						publish_message_to_sns(task_item['title'])
			
	return "Done!"