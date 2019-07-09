# Overdue

The goal of this Project is to create a temporary workaround for an implementation issue of Google Tasks, wherein it does not keep active reminders (at least on iOS) for overdue scheduled items. This project is set up a scheduled task to parse a set of Lists for overdue items and send a reminder for them.

Perhaps one day, it can be expanded to provide more helpful reminders, or perhaps act as a more general tool to translate features between services.

## Making Code Changes

The following command zips this project into a file that can be uploaded to a Lambda Function.

```
zip ../overdue.zip *
```
