# A. Preparation steps
**1. Install python packages**
````
pip install requests
pip install python-decouple
````
**2. Create an IAM user with policy `AmazonEC2ReadOnlyAccess`. From there, create an access keys**

**3. Create file to store environment variables. For demo only, input your keys into this file**

vi .env

````
AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
````
# B. Check code & run the 2 python files

# C. CleanUp
Don't forget to delete resources, especially access key

# D. Reference
[Create a signed AWS API request](https://docs.aws.amazon.com/IAM/latest/UserGuide/create-signed-request.html)
