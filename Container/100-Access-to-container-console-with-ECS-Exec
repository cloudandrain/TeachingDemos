**Reference**

- [Link 1](https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)
- [Link 2](https://www.ernestchiang.com/en/posts/2021/using-amazon-ecs-exec/)

**Initial lab information:** simply create an ECS cluster using sample template of nginx

1. Cluster name: `demo1-cluster1`
2. Service name: `nginx-service`
3. Task definition name: `demo1-task-definition`

>  Note: mind the revision number of task definition

Once the ECS cluster has created, go to its inside task to get public IP and then open by web browser

**Steps to access console**

#### 1. Configure IAM task role (NOT execution task role) as below:

   In Trusted entities, be careful the principal should be for `ecs-tasks`, NOT `ecs` 

````Trusted entities
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
````

````Inline policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel",
                "ecs:ExecuteCommand"
            ],
            "Resource": "*"
        }
    ]
}
````

#### 2. Update the service to use the newly-created IAM task role

#### 3. Enable `enableExecuteCommand` attribute of ECS service

Check if the `ECS service` has enabled the attribute `enableExecuteCommand` 

````
aws ecs describe-services --cluster demo1-cluster1 --services nginx-service
````

We can get task definition’s ARN from console or CLI

````
aws ecs describe-tasks --cluster  demo1-cluster1 --tasks 04bb794568c543dcb117e43b1dfd9983
````

Enable exe command in service + force new deployment.

The parameter for task definition is got from the above step

````
aws ecs update-service \
    --cluster demo1-cluster1 \
    --task-definition arn:aws:ecs:ap-southeast-2:696686700433:task-definition/demo1-task-definition:3 \
    --service nginx-service \
    --enable-execute-command \
    --force-new-deployment
````

#### 4. Execute command to enter bash shell console

````
aws ecs execute-command --cluster demo1-cluster1 \
    --task 04bb794568c543dcb117e43b1dfd9983 \
    --interactive \
    --command "/bin/bash"
````

Multiple containers in a task? --> use parameter `--container`

````Result
[cloudshell-user@ip-10-0-119-251 ~]$ aws ecs execute-command --cluster demo1-cluster1 \
>     --task 04bb794568c543dcb117e43b1dfd9983 \
>     --interactive \
>     --command "/bin/bash"

The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.


Starting session with SessionId: ecs-execute-command-051c01c432551ecfe
root@ip-10-0-0-119:/# 
root@ip-10-0-0-119:/# service nginx status
nginx is running.
root@ip-10-0-0-119:/# uname -a
Linux ip-10-0-0-119.ap-southeast-2.compute.internal 4.14.294-220.533.amzn2.x86_64 #1 SMP Thu Sep 29 01:01:23 UTC 2022 x86_64 GNU/Linux
root@ip-10-0-0-119:/#
root@ip-10-0-0-119:/# cat /etc/nginx/nginx.conf 

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
````
