# ToDo-2 Import Python Modules and Classes
import boto3
import requests
import csv

from dynamodb_encryption_sdk.encrypted.table import EncryptedTable
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider

from dynamodb_encryption_sdk.material_providers.wrapped import WrappedCryptographicMaterialsProvider
from dynamodb_encryption_sdk.delegated_keys.jce import JceNameLocalDelegatedKey
from dynamodb_encryption_sdk.identifiers import EncryptionKeyType, KeyEncodingType
from Crypto.Random import get_random_bytes

import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
from os import listdir


# ----------------------------------------------------------------
# Function Declarations - Main logic starts near bottom of script
# ----------------------------------------------------------------

# ToDo-3 Implement table-creation function
def create_spotlight_lab_table(new_table_name):

    print(f'Creating DynamoDB table {new_table_name}...')
    # creating the table with two schema (main) attributes: OrderID and Shipping Date
    table = dynamodb_client.create_table(
        TableName=new_table_name,
        KeySchema=[
            {
                'AttributeName': 'Order ID',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Ship Date',
                'KeyType': 'RANGE'  # Sort key
            }
        ], # Both schema elements are datatype 'string' - 'S'
        AttributeDefinitions=[
            {
                'AttributeName': 'Order ID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Ship Date',
                'AttributeType': 'S'
            }
         ],
        BillingMode='PAY_PER_REQUEST' # Using the 'fire and forget' Pay Per Request pricing strategy
    )
    waiter = dynamodb_client.get_waiter('table_exists')
    waiter.wait(TableName=new_table_name) # Waiting for the table to finish being created
    print(f'{new_table_name} creation complete.')
    return table

# ToDo-8 Implement on-prem key retrieval functions
def get_wrapping_key_from_on_prem_key_management_system():
    # Don't implement your program this way!
    # I'm pretending that we're getting keys from an on-prem system
    # for the purposes of this lab.  But I'm actually generating them locally
    new_wrapping_key = JceNameLocalDelegatedKey(
        key=get_random_bytes(32),
        algorithm='AES',
        key_type=EncryptionKeyType.SYMMETRIC,
        key_encoding=KeyEncodingType.RAW,
    )
    return new_wrapping_key

def get_signing_key_from_on_prem_key_management_system():
    # Don't implement your program this way!
    # I'm pretending that we're getting keys from an on-prem system
    # for the purposes of this lab.  But I'm actually generating them locally
    new_signing_key = JceNameLocalDelegatedKey(
        key=get_random_bytes(32),
        algorithm='HmacSHA512',
        key_type=EncryptionKeyType.SYMMETRIC,
        key_encoding=KeyEncodingType.RAW,
    )
    return new_signing_key

# ----------------------
# Main Application Logic
# ----------------------

# ToDo-1 - Identify AWS region and build Table 1

# Identify current AWS infrastructure Region
currentAWSRegion = (requests.get('http://169.254.169.254/latest/meta-data/placement/region')).text

# Build connection to DynamoDB service in the current region
dynamodb_client = boto3.client('dynamodb', currentAWSRegion)

if 'Table1' not in dynamodb_client.list_tables()['TableNames']:
    spotlightLabTable1 = create_spotlight_lab_table('Table1')

# ToDo-4 - Load Table 1 with sales data

#Connect to DynamoDB service
dynamodb_resource = boto3.resource('dynamodb', currentAWSRegion)

#Open Sales Data file
with open('./CSE/SKD-Encr/Data/50000SalesRecords.csv', 'rt') as f:
    salesDataReader = csv.DictReader(f)

    itemCount=0
    if dynamodb_resource.Table('Table1').scan()['ScannedCount'] == 0: #Wasteful action - don't do this in real life!.
        for salesRow in salesDataReader:
            if salesRow['Item Type'] == 'Office Supplies' and salesRow['Region'] == 'Europe':

                itemCount = itemCount + 1

                # Insert European Office Supply records into Table 1
                dynamodb_resource.Table('Table1').put_item(
                    Item={
                        'Region': salesRow['Region'],
                        'Country': salesRow['Country'],
                        'Item Type': salesRow['Item Type'],
                        'Sales Channel': salesRow['Sales Channel'],
                        'Order Priority': salesRow['Order Priority'],
                        'Order Date': salesRow['Order Date'],
                        'Order ID': salesRow['Order ID'],
                        'Ship Date': salesRow['Ship Date'],
                        'Units Sold': salesRow['Units Sold'],
                        'Unit Price': salesRow['Unit Price'],
                        'Unit Cost': salesRow['Unit Cost'],
                        'Total Revenue': salesRow['Total Revenue'],
                        'Total Cost': salesRow['Total Cost'],
                        'Total Profit': salesRow['Total Profit']
                    }
                )
                print(salesRow)
        print(f"\nInserted {itemCount} sales records into Table1")

# ToDo-5 - Create Table 2
        


#Create table 2 with helper table-creation function
if 'Table2' not in dynamodb_client.list_tables()['TableNames']:
    print("break 1")
    spotlightLabTable2 = create_spotlight_lab_table('Table2')

dynamodb_resource = boto3.resource('dynamodb', currentAWSRegion)
spotlightLabTable2 = dynamodb_resource.Table('Table2')

# ToDo-6 - Load Table2 with client-encrypted sales data using DynamoDB Encryption SDK and KMS Keys
# Open Sales Data file
with open('./CSE/SKD-Encr/Data/50000SalesRecords.csv', 'rt') as f:
    salesDataReader = csv.DictReader(f)

    itemCount=0
    # Create KMS Cryptographic Materials Provider
    spotlight_lab_direct_kms_cmp = AwsKmsCryptographicMaterialsProvider(
        'arn:aws:kms:ap-southeast-1:696686700433:key/6d57c86f-9228-4370-9cae-e198b1eb6594')

    # Create EncryptedTable object using table and CMP
    encrypted_table_access = EncryptedTable(
        table=spotlightLabTable2,
        materials_provider=spotlight_lab_direct_kms_cmp
    )
    if dynamodb_resource.Table('Table2').scan()['ScannedCount'] == 0: #Wasteful action - don't do this in real life!.
        for salesRow in salesDataReader:
            if int(salesRow['Units Sold']) < 1000 and salesRow['Region'] == 'North America':
                print(salesRow)
                itemCount = itemCount + 1
                # Issue item storage request to EncryptedTable object
                encrypted_table_access.put_item(
                    Item={
                        'Region': salesRow['Region'],
                        'Country': salesRow['Country'],
                        'Item Type': salesRow['Item Type'],
                        'Sales Channel': salesRow['Sales Channel'],
                        'Order Priority': salesRow['Order Priority'],
                        'Order Date': salesRow['Order Date'],
                        'Order ID': salesRow['Order ID'],
                        'Ship Date': salesRow['Ship Date'],
                        'Units Sold': salesRow['Units Sold'],
                        'Unit Price': salesRow['Unit Price'],
                        'Unit Cost': salesRow['Unit Cost'],
                        'Total Revenue': salesRow['Total Revenue'],
                        'Total Cost': salesRow['Total Cost'],
                        'Total Profit': salesRow['Total Profit']
                    }
                )
        print(f'\nInserted {itemCount} sales records into Table2')

# ToDo-7 - Create Table3 and use the DynamoDB Encryption Client with a Wrapped Materials Provider

#Connect to DynamoDB service and verify Table creation
dynamodb_resource = boto3.resource('dynamodb', currentAWSRegion)

#Create table 3 with helper table-creation function
if 'Table3' not in dynamodb_client.list_tables()['TableNames']:
    spotlightLabTable3 = create_spotlight_lab_table('Table3')
else:
    spotlightLabTable3 = dynamodb_resource.Table('Table3')
    dynamodb_resource = boto3.resource('dynamodb', currentAWSRegion)

    # Open Sales Data file
with open('./CSE/SKD-Encr/Data/50000SalesRecords.csv', 'rt') as f:

    salesDataReader = csv.DictReader(f)

    itemCount=0

    # Retrieve encryption keys from corporate key management system on premises
    private_wrapping_key = get_wrapping_key_from_on_prem_key_management_system()
    private_signing_key = get_signing_key_from_on_prem_key_management_system()

    # Assemble keys into a C.M.P.
    spotlight_lab_wrapped_cmp = WrappedCryptographicMaterialsProvider(
        wrapping_key=private_wrapping_key,
        unwrapping_key=private_wrapping_key,
        signing_key=private_signing_key
    )

    # Create EncryptedTable object by supplying table and CMP
    encrypted_table_access = EncryptedTable(
        table=dynamodb_resource.Table('Table3'),
        materials_provider=spotlight_lab_wrapped_cmp
    )

    # Load data about low-revenue vegetable sales into table 3
    if dynamodb_resource.Table('Table3').scan()['ScannedCount'] == 0: #Wasteful action - don't do this in real life!.
        for salesRow in salesDataReader:
            if float(salesRow['Total Revenue']) < 500000 and salesRow['Item Type'] == 'Vegetables':
                print(salesRow)
                itemCount = itemCount + 1
                # Issue item storage request to EncryptedTable object
                encrypted_table_access.put_item(
                    Item={
                        'Region': salesRow['Region'],
                        'Country': salesRow['Country'],
                        'Item Type': salesRow['Item Type'],
                        'Sales Channel': salesRow['Sales Channel'],
                        'Order Priority': salesRow['Order Priority'],
                        'Order Date': salesRow['Order Date'],
                        'Order ID': salesRow['Order ID'],
                        'Ship Date': salesRow['Ship Date'],
                        'Units Sold': salesRow['Units Sold'],
                        'Unit Price': salesRow['Unit Price'],
                        'Unit Cost': salesRow['Unit Cost'],
                        'Total Revenue': salesRow['Total Revenue'],
                        'Total Cost': salesRow['Total Cost'],
                        'Total Profit': salesRow['Total Profit']
                    }
                )
        print(f'\nInserted {itemCount} sales records into Table3')

# ToDo-9 - Use AWS Encryption SDK to protect local data
        
# Collect files from Grandma's secret recipes folder
recipes_directory = './CSE/SKD-Encr/Personal/'
recipe_file_list = listdir(recipes_directory)

for recipe in recipe_file_list:
    print('Encrypting ' + recipe)
    # Open a recipe file and read the text inside
    recipe_file = open(recipes_directory + recipe)
    recipe_text = recipe_file.read()
    recipe_file.close()

    # Create the AWS Encryption SDK client and attach it to a KMS Key
    client = aws_encryption_sdk.EncryptionSDKClient(commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)
    keys = dict(key_ids=['arn:aws:kms:ap-southeast-1:696686700433:key/6d57c86f-9228-4370-9cae-e198b1eb6594'])
    master_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(**keys)

    # Transform plain recipe text into encrypted recipe text
    ciphertext, encryptor_header = client.encrypt(source=recipe_text, key_provider=master_key_provider)

    # Store encrypted recipe bytes into new file
    new_recipe_file = open(recipes_directory + '[ENCRYPTED]-' + recipe, "wb")
    encrypted_file_content = bytearray(ciphertext)
    new_recipe_file.write(encrypted_file_content)
    new_recipe_file.close()
    print(' ... done.')
