To make requests to AWS, you must supply AWS credentials. Your code will find credentials to initialize a new service by following this priority order:

**1.  Credentials are specified in your code or CLI command**

Providing credentials within code or a CLI command will override settings in any other location.
You are enabled to also specify --region, --output, and --profile as parameters on the command line.

Ex:
````
aws configure set aws_access_key_id <yourAccessKey>
aws configure set aws_secret_access_key <yourSecretKey>
````

**2. Environment variables**
You can store values in your system's environment variables.  

**3. Default credentials file**
The credentials and config files are updated when you run the command aws configure.  
 
**4. Instance profile**
You can associate an IAM role with each of your EC2 instances.
- List itemTemporary credentials for that role are then available to code running in the instance.
- For more information on credentials, see the following:  
(Java) “Working with AWS Credentials” in the [AWS SDK for Java Developer Guide](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html)  
- (.NET) “Configuring AWS Credentials” in the [AWS SDK for .NET Developer Guide](https://docs.aws.amazon.com/sdk-for-net/v3/developer-guide/net-dg-config-creds.html)  
(Boto3) “Credentials” in the [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
