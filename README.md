# Overdue

The goal of this Project is to create a temporary workaround for an implementation issue of Google Tasks, wherein it does not keep active reminders (at least on iOS) for overdue scheduled items. This project is set up a scheduled task to parse a set of Lists for overdue items and send a reminder for them.

Perhaps one day, it can be expanded to provide more helpful reminders, or perhaps act as a more general tool to translate features between services.

## Making Code Changes

The following steps must be followed in order to create a deployable .zip file for Overdue.

### Generate token.pickle

First, create a file named `credentials.json` in your package root directory and add your Google API credentials to it.

Run the following command and copy/paste the URL provided. 

```
python3 generate_token.py
```

After properly authenticating, you should notice a file named `token.pickle` appear in the package root directory.

### Generate .zip file

The following command creates the .zip file and adds the package dependencies to it

```
cd packages
zip -r9 ../overdue.zip .
```

Next, run the following command to add the handler function code and your token to the .zip archive.

```
cd ../
zip -g overdue.zip index.py token.pickle
```

Done! Now you should have a complete `overdue.zip` file that you can upload to your Lambda Function.

## Configuring Lambda

After uploading the .zip archive to a created Lambda Function, there are only a few additional steps needed to get your own personal Function up and running.

1. Create an SNS Topic for this Function to publish to (and of course, subscribe to it)
1. Add the following Environment Variable to your Lambda Function: `SNS_ARN: <ARN of SNS topic from above step>`
1. Add the following IAM Permissions (via a new or existing IAM Role) to your Lambda Function: `AWSLambdaBasicExecutionRole` and `AWSLambdaSNSPublishPolicyExecutionRole`
1. Add a Cloudwatch Events trigger to your Lambda Function, and set it to occur at the desired interval (recommendation: `rate(1 day)`)