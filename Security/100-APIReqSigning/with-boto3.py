import boto3
import json
import os

ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
response = ec2.vpcs.filter(
    Filters=[
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        },
    ],
)
for vpc in response:
    print(vpc.vpc_id,vpc.cidr_block)