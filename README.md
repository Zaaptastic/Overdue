# Overdue

The goal of this Project is to create a temporary workaround for an implementation issue of Google Tasks, wherein it does not keep active reminders (at least on iOS) for overdue scheduled items. This project is set up a scheduled task to parse a set of Lists for overdue items and send a reminder for them.

Perhaps one day, it can be expanded to provide more helpful reminders, or perhaps act as a more general tool to translate features between services.

## Making Code Changes

The following steps must be followed in order to create a deployable .zip file for Overdue.

### Generate Authentication Token

First, create a file named `credentials.json` in your package root directory and add your Google API credentials to it.

Run the following command and copy/paste the URL provided. 

```
python3 generate_token.py
```

After properly authenticating, you should notice a file named `token.pickle` appear in the package root directory. Upload this token to a dedicated, private bucket on S3.

### Running Unit Tests

To execute the unit testing suite, simply run the command:

```
python3 lambda_tests.py
```

### Running Deployment Script
Assuming you have your AWS CLI correctly configured, you can take advantage of a handy script provided in the root package directory to easily test, build, and deploy your Lambda Function. Simply run the command:

```
python3 deploy_lambda_function.py
```

### Generate .zip file

The following command creates the .zip file and adds the package dependencies to it

```
cd package
zip -r9 ../overdue.zip .
```

Next, run the following command to add the handler function code and your token to the .zip archive.

```
cd ../
zip -g overdue.zip lambda_handler.py
```

Done! Now you should have a complete `overdue.zip` file that you can upload to your Lambda Function.

## Configuring Lambda

After uploading the .zip archive to a created Lambda Function, there are only a few additional steps needed to get your own personal Function up and running.

1. Create an SNS Topic for this Function to publish to (and of course, subscribe to it)
1. Add the following Environment Variables to your Lambda Function:
    1. Key: `SNS_ARN`, Value: `<ARN of SNS topic from above step>`
    1. Key: `S3_BUCKET_NAME`, Value: `<Name of S3 Bucket containing authentication token>`
    1. Key: `S3_FILE_NAME`, Value: `<Name of authentication token file>`
1. Add the following IAM Permissions (via a new or existing IAM Role) to your Lambda Function: `AWSLambdaBasicExecutionRole`, `AmazonS3ReadOnlyAccess` and `AWSLambdaSNSPublishPolicyExecutionRole`
1. Add a Cloudwatch Events trigger to your Lambda Function, and set it to occur at the desired interval (recommendation: `rate(1 day)`)