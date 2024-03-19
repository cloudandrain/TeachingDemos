
1. Tạo 2 IAM users: `lab-u1` & `lab-u2`, tương ứng được quyền vào `marketing` & `sales`.
   - Không cần gắn với policy nào hết
   - Chọn programmatic acesss
2. Bucket có sẵn 2 prefixes (marketing & sales) và objects

````
AccessPoint % ls -R
marketing	sales

./marketing:
1.txt	2.txt

./sales:
1.txt
````

**S3 bucket policy**: chỉ cho truy xuất thông qua Access Point của 1 tài khoản AWS chỉ định. Chúng ta có thể kiểm soát thông qua [AP ARN](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html#amazons3-s3_DataAccessPointArn)

````
{
    "Version": "2012-10-17",
    "Id": "Policy1669521251267",
    "Statement": [
        {
            "Sid": "Stmt1669521248488",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::lab-s3bucket-0064",
                "arn:aws:s3:::lab-s3bucket-0064/*"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:DataAccessPointAccount": "696686700433"
                }
            }
        }
    ]
}
````

3. S3 `Access point policies` (marketing & sales)

````s3ap-en
{
    "Version": "2012-10-17",
    "Id": "Policy1",
    "Statement": [
        {
            "Sid": "Stmt1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::696686700433:user/lab-u1"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:ap-southeast-1:696686700433:accesspoint/s3ap-marketing/object/marketing/*"
        }
    ]
}
````

````s3ap-fr
{
    "Version": "2012-10-17",
    "Id": "Policy1",
    "Statement": [
        {
            "Sid": "Stmt1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::696686700433:user/lab-u2"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:ap-southeast-1:696686700433:accesspoint/s3ap-sales/object/sales/*"
        }
    ]
}
````

4. Kiểm tra

- Login vào lab-u2, download file trực tiếp:

````
sutrinh@3c063001203c AccessPoint % aws s3api get-object --key sales/1.txt --bucket lab-s3bucket-0064 downloaded-sales-1.txt 

An error occurred (AccessDenied) when calling the GetObject operation: Access Denied
````

- Download thông qua AP

````
sutrinh@3c063001203c AccessPoint % aws s3api get-object --key sales/1.txt --bucket arn:aws:s3:ap-southeast-1:696686700433:accesspoint/s3ap-sales downloaded-sales-1.txt
{
    "AcceptRanges": "bytes",
    "LastModified": "2022-11-27T03:44:53+00:00",
    "ContentLength": 8,
    "ETag": "\"894dddf3304cbcb0fe04f7c2bbd56073\"",
    "ContentType": "text/plain",
    "Metadata": {}
}
sutrinh@3c063001203c AccessPoint % cat downloaded-sales-1.txt 
Bonjour

````

- Can also download via Alias

````Can also download via Alias
sutrinh@3c063001203c AccessPoint % aws s3api get-object --key sales/1.txt --bucket s3ap-sales-fcq9tswi6fgos4hcchcmi8a9fqewgaps1a-s3alias downloaded-sales-1-viaAlias.txt
{
    "AcceptRanges": "bytes",
    "LastModified": "2022-11-27T03:44:53+00:00",
    "ContentLength": 8,
    "ETag": "\"894dddf3304cbcb0fe04f7c2bbd56073\"",
    "ContentType": "text/plain",
    "Metadata": {}
}
sutrinh@3c063001203c AccessPoint % ls
downloaded-sales-1-viaAlias.txt	en
downloaded-sales-1.txt		fr
sutrinh@3c063001203c AccessPoint % cat downloaded-fr-1-viaAlias.txt 
Bonjour
sutrinh@3c063001203c AccessPoint %
````

aws s3api get-object --key fr/1.txt --bucket arn:aws:s3:ap-southeast-1:696686700433:accesspoint/s3apinsidepvc downloaded-fr-1.txt

- Upload thông qua AP

````
sutrinh@3c063001203c AccessPoint % aws s3api put-object --key marketing/3.txt --bucket arn:aws:s3:ap-southeast-1:696686700433:accesspoint/s3ap-marketing --body ./en/3.txt
{
    "ETag": "\"05fefbc5f01599c2faebe5e26446de4e\""
}
````



````
{
    "Version": "2012-10-17",
    "Id": "Policy1669521578263",
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::696686700433:user/alice"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::lab-s3bucket-0064/marketing",
                "arn:aws:s3:::lab-s3bucket-0064/marketing/*"
            ]
        },
        {
            "Sid": "2",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::696686700433:user/bob"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::lab-s3bucket-0064/sales",
                "arn:aws:s3:::lab-s3bucket-0064/sales/*"
            ]
        }
    ]
}
````
