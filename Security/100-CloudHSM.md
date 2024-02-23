<span style="font-size:4em;">Configure CloudHSM cluster</span>

- [High-level steps](#high-level-steps)
- [Low-level steps](#low-level-steps)
  * [1.  Create HSM Cluster](#1--create-hsm-cluster)
  * [2.  Initialize HSM cluster](#2--initialize-hsm-cluster)
  * [3. Download Cluster CSR](#3-download-cluster-csr)
  * [4. Create key, certificate & sign the CSR](#4-create-key--certificate---sign-the-csr)
  * [5. Upload certificates to completing the initialization](#5-upload-certificates-to-completing-the-initialization)
  * [6. Activate the HSM cluster](#6-activate-the-hsm-cluster)
  * [7. Login to HSM and change password](#7-login-to-hsm-and-change-password)
- [References](#references)

# High-level steps

**Preparation**

1. Add IAM role
**
AWS side**

1.  Create HSM Cluster
2.  Initialize the cluster
3.  Download ClusterCSR (certificate signing request)

**EC2 instance side (or can use Cloud9)**

4. Create key, certificate & sign the CSR (EC2 instance side)

   1.  Create Pri key LOCALLY

   1.  From the created Pri key, create a CA certificate

   1.  Sign the CSR. Input is the downloaded HSM cluster CSR.

5. [Upload certificates to completing the initialization](#5.-Upload-certificates-to-completing-the-initialization) (either using CLI or directly on AWS console)

6. Activate the HSM cluster (EC2 instance side)

   1.  Download & install HSM client

   2.  Edit Client configuration by updating the HSM's IP address

7. Login into HSM with PRECO user and change password (EC2 instance side)

# Low-level steps

## 1.  Create HSM Cluster

## 2.  Initialize HSM cluster

    To initialize the cluster, you must first create an HSM in the cluster.
    
    Choose the Availability Zone to create this HSM

## 3. Download Cluster CSR

Create HSM user with permission to initialize the cluster. Only in lab, choose **FullAccess** for simple. Use the credential to proceed next CLI steps

````
export HSM_CLUSTER_ID=cluster-xwmvjy6wplk

aws cloudhsmv2 describe-clusters \
--filters clusterIds=$HSM_CLUSTER_ID \
--output text --query 'Clusters[].Certificates.ClusterCsr' > myClusterCsr.csr
````

## 4. Create key, certificate & sign the CSR

a. Create Pri key LOCALLY
````
openssl genrsa -aes256 -out CAPriKey.key 2024
````

b. From the created Pri key, create a CA certificate
  ````
openssl req -new -x509 -days 365 -key CAPriKey.key -out customerCA.crt
  ````

> The output `customerCA.crt` is known as `Trust anchor`

 c. Sign the CSR. Input is the downloaded HSM cluster CSR.
  ````
openssl x509 -req -days 365 -in myClusterCsr.csr -CA customerCA.crt -CAkey CAPriKey.key -CAcreateserial -out CustomerHsmCert.crt 
  ````


## 5. Upload certificates to completing the initialization

This can be done either by AWS Console or CLI

If you prefer CLI, use following command
````
aws cloudhsmv2 initialize-cluster --cluster-id $HSM_CLUSTER_ID --signed-cert file://CustomerHsmCert.crt --trust-anchor file://customerCA.crt
````

## 6. Activate the HSM cluster

  a. [Download & install HSM client](https://docs.aws.amazon.com/cloudhsm/latest/userguide/kmu-install-and-configure-client-linux.html)

````
wget https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL6/cloudhsm-client-latest.el6.x86_64.rpm

sudo yum install ./cloudhsm-client-latest.el6.x86_64.rpm
````

  b. Edit Client configuration by updating the HSM's IP address

````
$ sudo cp customerCA.crt /opt/cloudhsm/etc/customerCA.crt
````

Find IP directly in the Console
![6de89255bb041490f621467b7193d638.png](:/0bc265e482df48968fc151f6963fbb2a)


````
$ sudo /opt/cloudhsm/bin/configure -a 10.10.4.20

Updating server config in /opt/cloudhsm/etc/cloudhsm_client.cfg
Updating server config in /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg

$ cat /opt/cloudhsm/etc/cloudhsm_client.cfg
{
    "client": {
        "CriticalAlertScript": "",
        "create_object_minimum_nodes": 1,
        "daemon_id": 1,
        "e2e_owner_crt_path": "/opt/cloudhsm/etc/customerCA.crt",
        "enable_3des_key_reuse": "no",
        "log_level": "INFO",
        "reconnect_attempts": -1,
        "reconnect_interval": 3,
        "socket_type": "UNIXSOCKET",
        "sslreneg": 0,
        "tcp_port": 1111,
        "workers": 1,
        "zoneid": 0
    },
    "dualfactor": {
        "certificate": "certificate.crt",
        "dualfactor_ch_ssl_ciphers": "default",
        "dualfactor_ssl": "yes",
        "enable": "no",
        "pkey": "pkey.pem",
        "port": 2225
    },
    "loadbalance": {
        "enable": "yes",
        "prefer_same_zone": "no",
        "relative_idleness_weight": 1,
        "sucess_rate_weight": 1
    },
    "server": {
        "hostname": "10.10.4.20",
        "port": 2223
    },
    "ssl": {
        "CApath": "/opt/cloudhsm/etc/certs",
        "certificate": "/opt/cloudhsm/etc/client.crt",
        "pkey": "/opt/cloudhsm/etc/client.key",
        "server_ch_ssl_ciphers": "default",
        "server_ssl": "yes"
    }
}[cloudshell-user@ip-10-130-42-71 hsmlab]$ cat /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
{
    "scard": {
        "certificate": "cert-sc",
        "enable": "no",
        "pkey": "pkey-sc",
        "port": 2225
    },
    "servers": [
        {
            "CAfile": "",
            "CApath": "/opt/cloudhsm/etc/certs",
            "certificate": "/opt/cloudhsm/etc/client.crt",
            "e2e_encryption": {
                "enable": "yes",
                "owner_cert_path": "/opt/cloudhsm/etc/customerCA.crt"
            },
            "enable": "yes",
            "hostname": "10.10.4.20",
            "name": "10.10.4.20",
            "pkey": "/opt/cloudhsm/etc/client.key",
            "port": 2225,
            "server_ssl": "yes",
            "ssl_ciphers": ""
        }
    ]
}


````

## 7. Login to HSM and change password

After changing password, the user type changes from PRECO (PRECrypto Officer) to CO

  a. **Start** the CloudHSM Mgmt Utility (CMU) CLI
````
/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
````

  b. Modify security group allowing port range 2223-2225


  c. Login into HSM with PRECO user and change password

````
aws-cloudhsm>loginHSM PRECO admin password
loginHSM success on server 0(10.10.4.20)

aws-cloudhsm>loginHSM PRECO admin password
loginHSM success on server 0(10.10.4.20)
aws-cloudhsm>listUsers
Users on server 0(10.10.4.20):
Number of users found:2

    User Id             User Type       User Name                          MofnPubKey    LoginFailureCnt         2FA
         1              PRECO           admin                                    NO               0               NO
         2              AU              app_user                                 NO               0               NO


aws-cloudhsm>
````

Change password with command `changePswd PRECO admin P@55w0rd`
````
aws-cloudhsm>changePswd PRECO admin P@55w0rd
*************************CAUTION********************************
This is a CRITICAL operation, should be done on all nodes in the
cluster. AWS does NOT synchronize these changes automatically with the 
nodes on which this operation is not executed or failed, please 
ensure this operation is executed on all nodes in the cluster.  
****************************************************************

Do you want to continue(y/n)?y
Changing password for admin(PRECO) on 1 nodes
changePswd success on server 0(10.10.4.20)

````

Notice that the type changed from `PRECO` to `CO`
````
aws-cloudhsm>listUsers
Users on server 0(10.10.4.20):
Number of users found:2

    User Id             User Type       User Name                          MofnPubKey    LoginFailureCnt         2FA
         1              CO              admin                                    NO               0               NO
         2              AU              app_user                                 NO               0               NO
````

# References

- https://docs.aws.amazon.com/kms/latest/developerguide/create-keystore.html
- https://aws.amazon.com/blogs/security/understanding-aws-cloudhsm-cluster-synchronization/
- https://docs.aws.amazon.com/cloudhsm/latest/userguide/cloudhsm_mgmt_util-getting-started.html
