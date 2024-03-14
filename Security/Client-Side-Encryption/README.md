# Preparation
1. Check Python version
$ python
Python 3.8.16 (default, Aug 30 2023, 23:19:34)

2. Create role `viewerInstanceRoleForMedicalImages` which is applied to Cloud9 instance
Policies:
- AmazonSSMManagedInstanceCore (managed)
- viewerInstancePolicySettingsForMedicalImages (inline)

````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListAccessPointsForObjectLambda",
                "s3:describe*",
                "s3:GetObjectVersionTagging",
                "s3:ListStorageLensGroups",
                "s3:GetStorageLensConfigurationTagging",
                "s3:GetObjectAcl",
                "s3:GetBucketObjectLockConfiguration",
                "s3:GetIntelligentTieringConfiguration",
                "s3:GetStorageLensGroup",
                "s3:GetAccessGrantsInstanceForPrefix",
                "s3:GetObjectVersionAcl",
                "s3:GetBucketPolicyStatus",
                "s3:GetAccessGrantsLocation",
                "s3:GetObjectRetention",
                "s3:GetBucketWebsite",
                "s3:GetJobTagging",
                "s3:ListJobs",
                "s3:GetMultiRegionAccessPoint",
                "s3:GetObjectAttributes",
                "s3:GetAccessGrantsInstanceResourcePolicy",     
                "s3:GetObjectLegalHold",
                "s3:GetBucketNotification",
                "s3:DescribeMultiRegionAccessPointOperation",
                "s3:GetReplicationConfiguration",
                "s3:ListMultipartUploadParts",
                "s3:GetObject",
                "s3:DescribeJob",
                "s3:GetAnalyticsConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetAccessPointForObjectLambda",
                "s3:GetStorageLensDashboard",
                "s3:GetLifecycleConfiguration",
                "s3:GetAccessPoint",
                "s3:GetInventoryConfiguration",
                "s3:GetBucketTagging",
                "s3:GetAccessPointPolicyForObjectLambda",
                "s3:GetBucketLogging",
                "s3:ListBucketVersions",
                "s3:GetAccessGrant",
                "s3:ListBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetObjectVersionAttributes",
                "s3:GetBucketPolicy",
                "s3:ListTagsForResource",
                "s3:GetEncryptionConfiguration",
                "s3:GetObjectVersionTorrent",
                "s3:list*",
                "s3:GetBucketRequestPayment",
                "s3:ListAccessGrantsInstances",
                "s3:ListAccessGrants",
                "s3:GetAccessPointPolicyStatus",
                "s3:GetAccessGrantsInstance",
                "s3:GetObjectTagging",
                "s3:GetMetricsConfiguration",
                "s3:GetBucketOwnershipControls",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetMultiRegionAccessPointPolicyStatus",
                "s3:putobject*",
                "s3:ListBucketMultipartUploads",
                "s3:GetMultiRegionAccessPointPolicy",
                "s3:GetAccessPointPolicyStatusForObjectLambda",
                "s3:ListAccessPoints",
                "s3:GetDataAccess",
                "s3:GetBucketVersioning",
                "s3:ListMultiRegionAccessPoints",
                "s3:GetBucketAcl",
                "s3:GetAccessPointConfigurationForObjectLambda",
                "s3:ListAccessGrantsLocations",
                "s3:ListStorageLensConfigurations",
                "s3:GetObjectTorrent",
                "s3:GetMultiRegionAccessPointRoutes",
                "s3:GetStorageLensConfiguration",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:getobject*",
                "s3:GetBucketCORS",
                "s3:GetBucketLocation",
                "s3:GetAccessPointPolicy",
                "s3:GetObjectVersion",
                "dynamodb:PutItem",
                "dynamodb:DescribeTable",
                "dynamodb:Scan",
                "dynamodb:CreateTable",
                "dynamodb:Query",
                "dynamodb:ListTables",
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateKey"
            ],
            "Resource": "*"
        }
    ]
}
````

3. Initial installation on Cloud9 instance
pip install boto3
pip install requests

**To use AWS Encryption SDK**
````
pip install dynamodb-encryption-sdk
pip install aws_encryption_sdk
pip install -U PyCryptodome
pip install Crypto
````
# SSE, Table1
By default, DynamoDB automatically delivers server-side encryption of data. The items you are seeing represent encrypted data stored in DynamoDB. DynamoDB SSE automatically decrypted those items in response to your request to view them. So no administrative effort

This is done by *ToDo4*: connect to the DynamoDB service, read a CSV file looking for sales of office supplies to Europe, and insert those data items into Table1 in DynamoDB

# CSE
Implementing client-side encryption adds complexity to a project, but may be a requirement of some workloads. Let's discover a couple of different varieties of client-side encryption. Here, I introduce 3 techniques

## Technique 1, Table2 - *ToDo6* - Load Table2 with client-encrypted sales data using DynamoDB Encryption SDK and KMS Keys
1. Create new KMS key. Remember to grant permission for KMS Key user (the role which is applied to Cloud9 instance)
2. Utilize an AWS KMS key to create a resource called a Cryptographic Materials Provider (CMP)
3. Verification
    a. Only the first two attributes (keys) are readable for the displayed items. The remaining attributes remain encrypted. Also note that the DynamoDB Encryption SDK has added two additional attributes, *amzn-ddb-map-desc* and *amzn-ddb-map-sig*.
    b. The items you are seeing contain CSE data. DynamoDB is unable to decrypt these items. These items can only be decrypted by client-side code like what you used to create these encrypted resources.


## Technique 2, Table3 - *ToDo7* - NOT using KMS, create Table 3 and use the DynamoDB Encryption Client with a Wrapped Materials Provider.
1. ToDo8 - Implement on-prem key retrieval functions. For the purposes of this lab, we simulate getting keys from an on-prem system but actually generating them locally
2. ToDo7 - Create Table3 and use the DynamoDB Encryption Client with a Wrapped Materials Provider

## Technique 3 - use AWS Encryption SDK to encrypt any ARBITRARY data (not just data on AWS) with an AWS KMS key.
