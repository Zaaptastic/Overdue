import overdue_tasks_lambda_handler
	
def overdue_tasks_handler(event, context):
	print("Beginning Lambda Handler Execution for Overdue Tasks.")
	return overdue_tasks_lambda_handler.handle_overdue_tasks(event, context)
