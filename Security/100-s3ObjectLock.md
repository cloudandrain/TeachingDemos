# Summary

- Object Lock **works only on Versioned buckets.** You must enable Versioning on this bucket before you can enable Object Lock.
- Then enable object lock. Once enabled, you can't disable Object Lock or suspend Versioning for the bucket.
- If we delete the object "delete marker", it returns to non-versioned object
- Object lock settings can be configured at bucket-level or object-level
    - When uploading object to S3 bucket using the AWS console, object Lock settings can't be specified.
    - If you still want, use AWS CLI, AWS SDK or Amazon S3 REST API or configure object settings after uploading.

S3 Object lock comes up with 3 modes:

## 1. Legal hold

- Once set, we can delete the object but then it create a version of it with "delete marker"
- We then can't delete the versioned object

## 2. Governance mode - with retention

&nbsp;

## 3. Compliance mode - with retention

- - Once set, we cannot do anything except from extending the retained period

# Lab steps



## 1. Create IAM policy, user with restricted S3 actions

Environment variables

export BUCKET_NAME="..."
export REGION="ap-southeast-1"
export IAM_POLICY="lab-objectLock-basicPermissions"

If not existed, create new bucket
````
aws s3api create-bucket \
   --bucket $BUCKET_NAME \
   --region $REGION \
````

Enable bucket versioning
````
aws s3api put-bucket-versioning \
   --bucket $BUCKET_NAME \
   --versioning-configuration Status=Enabled \
````

````
cat > IAM_POLICY << "EOF"
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Sid": "VisualEditor0",
           "Effect": "Allow",
           "Action": [
               "s3:PutObject",
               "s3:PutObjectRetention",
               "s3:Get*",
               "s3:PutObjectLegalHold",
               "s3:DeleteObject",
               "s3:DeleteObjectVersion",
               "s3:List*",
               "s3:DeleteBucket",
               "s3:Describe*"
           ],
           "Resource": "*"
       }
   ]
}
EOF
````


- LegalHold: `s3:PutObjectLegalHold`
- Enable retention
    - `s3:PutObjectRetention`
    - `s3:PutBucketObjectLockConfiguration`
- To delete versioned object: `s3:DeleteObjectVersion`

## 2. Upload v1 objects and change object locks settings

| File name | Object lock settings |
| --------- | -------------------- |
| 1.txt     | Legal hold           |
| 2.txt     | Governance           |
| 3.txt     | Compliance           |
| 4.txt     | Governance           |

## 2\. Update the files with the same names

New versions will be created

## 3\. Delete v1 objects by... AWS CLI

Command

```
aws s3api delete-object --bucket my-bucket --key <FileName> --version-id <Version_ID>
```

All deletions results in `Access Denied` as expected

Sample script:

```
aws s3api delete-object --bucket lab0064-bucket2 --key 1.txt --version-id wQi_GzYG_OPG14KZlVXcpoIc4pESIErn

An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied

---
aws s3api delete-object --bucket lab0064-bucket2 --key 2.txt --version-id 4IvneGsGO2hRtFbCChu4yOpja5UTZLCb

An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied

---
aws s3api delete-object --bucket lab0064-bucket2t --key 3.txt --version-id YXsawWKmamGir_CpejRcvk0RAp_6q55e

An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied
sutrinh@3c063001203c 100-S3ObjectLock % 
```

## 4\. Try disable Object Lock settings of v1 objects and delete again

- Delete 1-3.txt; Keep 4.txt intacted
- Successful delete `1.txt` & `2.txt`
- Notice that we can **NOT** change `compliance` mode `3.txt`, neither delete it.

Sample script:

```
aws s3api delete-object --bucket lab0064-bucket2 --key 1.txt --version-id wQi_GzYG_OPG14KZlVXcpoIc4pESIErn
{
    "VersionId": "wQi_GzYG_OPG14KZlVXcpoIc4pESIErn"
}

---
aws s3api delete-object --bucket lab0064-bucket2 --key 2.txt --version-id 4IvneGsGO2hRtFbCChu4yOpja5UTZLCb 
{
    "VersionId": "4IvneGsGO2hRtFbCChu4yOpja5UTZLCb"
}

---
aws s3api delete-object --bucket lab0064-bucket2 --key 3.txt --version-id YXsawWKmamGir_CpejRcvk0RAp_6q55e 

An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied
sutrinh@3c063001203c 100-S3ObjectLock % 
```

## 5\. Discover deletion difference between using AWS CLI & AWS Console

We uploaded `4.txt`

### a. Using CLI, try to delete `4.txt` to create a version

```
sutrinh@3c063001203c 100-S3ObjectLock % aws s3api delete-object --bucket lab0064-bucket2 --key 4.txt {
    "DeleteMarker": true,
    "VersionId": "x2moJ5HrfZiMqMqdDLggUvdAfCQDeXxz"
}

```

### b. Change to the versioned object's setting to `governance` mode

### c. Using AWS console, try to delete `4.txt` again

```
aws s3api delete-object --bucket lab0064-bucket2 --key 4.txt --version-id 2J0JNI37F4hlMjxH_2DPxEa6hK7DA1Ld

An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied
```


The explanation is [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html):

> By default, the Amazon S3 console includes the `x-amz-bypass-governance-retention:true` header. If you try to delete objects protected by governance mode and have the `s3:BypassGovernanceRetention` permission, the operation will succeed.

### d. Make deletion with CLI command successful

i. Add permission `s3:BypassGovernanceRetention` to IAM user  
ii. Append the option `--bypass-governance-retention` in the CLI command

````
aws s3api delete-object --bucket lab0064-bucket2 --key 4.txt --version-id Htc95_u9ckqpbPtnKR2wuJ0_CkF9ztOo --bypass-governance-retention    
{
    "VersionId": "Htc95_u9ckqpbPtnKR2wuJ0_CkF9ztOo"
}
````


Review the IAM policy
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectRetention",
                "s3:DeleteObjectVersion",
                "s3:Get*",
                "s3:PutObjectLegalHold",
                "s3:DeleteObject",
                "s3:List*",
                "s3:DeleteBucket",
                "s3:Describe*",
                "s3:BypassGovernanceRetention"
            ],
            "Resource": "*"
        }
    ]
}
````