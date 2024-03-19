**Purpose**: for your auditing and analysis only.

# Steps

1. AWS Config --> Settings

   - Enable recording with specific resource types. Ex: EC2

   - Specify SNS topic name. Ex: `awsconfig-lab`

   - Specify S3 bucket to contain conf history, snapshot. Common format: `config-bucket-XXXXXXXX/AWSLogs/<AccountID>/Config/<Region>/YYYY/MM/DD`

   - Initally, in the S3 bucket, we only see object `ConfigWritabilityCheckFile`

     > AWS Config creates this file to verify that the service has permissions to successfully write to the S3 bucket.

2. To **verify that your configuration recorder** has the settings that you want

````
aws configservice describe-configuration-recorders --region ap-southeast-1

{
    "ConfigurationRecorders": [
        {
            "name": "default",
            "roleARN": "arn:aws:iam::696686700433:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            "recordingGroup": {
                "allSupported": false,
                "includeGlobalResourceTypes": false,
                "resourceTypes": [
                    "AWS::EC2::Instance"
                ]
            }
        }
    ]
}
````

3. Check File delivery status. Mind the `configHistoryDeliveryInfo` (Enabled when you set up the configuration recorder.) & `configSnapshotDeliveryInfo`

````
aws configservice describe-delivery-channel-status --region ap-southeast-1
{
    "DeliveryChannelsStatus": [
        {
            "name": "default",
            "configSnapshotDeliveryInfo": {},
            "configHistoryDeliveryInfo": {
                "lastStatus": "FAILURE",
                "lastErrorCode": "NoSuchBucket",
                "lastErrorMessage": "An exception occurred while trying to deliver data to your Amazon S3 bucket. The specified Bucket does not exist.",
                "lastAttemptTime": "2023-02-28T14:48:40.549000+07:00",
                "lastSuccessfulTime": "2022-04-08T15:05:21.934000+07:00"
            },
            "configStreamDeliveryInfo": {
                "lastStatus": "SUCCESS",
                "lastStatusChangeTime": "2023-02-28T16:21:58.810000+07:00"
            }
        }
    ]
}
````

4. We will use AWS CLI `put-delivery-channel` to enable configuration snapshot.

- Create “skeleton” file `deliveryChannel.json`. Here we configure the frequency <u>1 hour</u>

````
{
    "name": "default",
    "s3BucketName": "config-bucket-sgp",
    "snsTopicARN": "arn:aws:sns:ap-southeast-1:696686700433:awsconfig-lab",
    "configSnapshotDeliveryProperties": {
        "deliveryFrequency": "One_Hour"
    }
}
````

- Execute the command  `put-delivery-channel`. A successul command results in nothing

````
aws configservice put-delivery-channel --delivery-channel file://deliveryChannel.json --region ap-southeast-1
````

To view the configuration of channel

````
aws configservice describe-delivery-channels --region ap-southeast-1
{
    "DeliveryChannels": [
        {
            "name": "default",
            "s3BucketName": "config-bucket-sgp",
            "snsTopicARN": "arn:aws:sns:ap-southeast-1:696686700433:awsconfig-lab",
            "configSnapshotDeliveryProperties": {
                "deliveryFrequency": "Twelve_Hours"
            }
        }
    ]

````





3. Again, `describe-delivery-channel-status` will see new thing of `configSnapshotDeliveryInfo`

````
aws configservice describe-delivery-channel-status --region ap-southeast-1
{
    "DeliveryChannelsStatus": [
        {
            "name": "default",
            "configSnapshotDeliveryInfo": {
                "nextDeliveryTime": "2023-02-28T17:43:59.190000+07:00"
            },
            "configHistoryDeliveryInfo": {
                "lastStatus": "FAILURE",
                "lastErrorCode": "NoSuchBucket",
                "lastErrorMessage": "An exception occurred while trying to deliver data to your Amazon S3 bucket. The specified Bucket does not exist.",
                "lastAttemptTime": "2023-02-28T14:48:40.549000+07:00",
                "lastSuccessfulTime": "2022-04-08T15:05:21.934000+07:00"
            },
            "configStreamDeliveryInfo": {
                "lastStatus": "SUCCESS",
                "lastStatusChangeTime": "2023-02-28T17:05:25.744000+07:00"
            }
        }
    ]
}
````

5. If we want to **configure Config-Snapshot on-demand instead of waiting** for next period of update, use AWS CLI `deliver-config-snapshot`

   

````
aws configservice deliver-config-snapshot --delivery-channel-name default --region ap-southeast-1

{
    "configSnapshotId": "3be1b995-e119-4d84-935f-dae2dc00b693"
}
````

	6. **Verify again** by CLI, as well as check new object on S3 bucket

````
aws configservice describe-delivery-channel-status --region ap-southeast-1
{
    "DeliveryChannelsStatus": [
        {
            "name": "default",
            "configSnapshotDeliveryInfo": {
                "lastStatus": "SUCCESS",
                "lastAttemptTime": "2023-02-28T22:50:20.939000+00:00",
                "lastSuccessfulTime": "2023-02-28T22:50:20.939000+00:00",
                "nextDeliveryTime": "2023-03-01T10:50:19.869000+00:00"
            },
            "configHistoryDeliveryInfo": {
                "lastStatus": "SUCCESS",
                "lastAttemptTime": "2023-02-28T21:16:19.674000+00:00",
                "lastSuccessfulTime": "2023-02-28T21:16:19.674000+00:00"
            },
            "configStreamDeliveryInfo": {
                "lastStatus": "SUCCESS",
                "lastStatusChangeTime": "2023-03-01T03:05:25.353000+00:00"
            }
        }
    ]
}
````

Download the file from S3, this is a part of record of EC2 instance 

| 138                          |                                                    |
| ---------------------------- | -------------------------------------------------- |
| relatedEvents                | []                                                 |
| relationships                | […]                                                |
| configuration                | {…}                                                |
| supplementaryConfiguration   | {}                                                 |
| tags                         | {…}                                                |
| configurationItemVersion     | "1.3"                                              |
| configurationItemCaptureTime | "2023-02-28T03:44:31.656Z"                         |
| configurationStateId         | 1677555871656                                      |
| awsAccountId                 | "696686700433"                                     |
| configurationItemStatus      | "OK"                                               |
| resourceType                 | "AWS::EC2::Instance"                               |
| resourceId                   | "i-0b247d47f516b6727"                              |
| ARN                          | "arn:aws:ec2:ap-southeast…nce/i-0b247d47f516b6727" |
| awsRegion                    | "ap-southeast-1"                                   |
| availabilityZone             | "ap-southeast-1a"                                  |
| configurationStateMd5Hash    | ""                                                 |
| resourceCreationTime         | "2023-02-28T03:30:15.000Z"                         |

#### Ref

- [Understanding the differences between configuration history and configuration snapshot files in AWS Config](https://aws.amazon.com/blogs/mt/configuration-history-configuration-snapshot-files-aws-config/)
- [Managing AWS Resource Configurations and History](https://docs.aws.amazon.com/config/latest/developerguide/manage-config.html)
- [Viewing AWS Resource Configurations and History](https://docs.aws.amazon.com/config/latest/developerguide/view-manage-resource.html)
- To enable configuration snapshot: [`put-delivery-channel`](https://docs.aws.amazon.com/cli/latest/reference/configservice/put-delivery-channel.html)
- To schedule delivery of a configuration snapshot: [`deliver-config-snapshot`](https://docs.aws.amazon.com/cli/latest/reference/configservice/deliver-config-snapshot.html#deliver-config-snapshot)
- To view the configuration of channel: [`describe-delivery-channels`](https://docs.aws.amazon.com/cli/latest/reference/configservice/describe-delivery-channels.html#examples)
