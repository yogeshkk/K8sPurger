<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# K8SPurger

## A Simple script to hunt and delete unused Kubernetes resources such as Secret, ConfigMap, and Persistent Volume Claim

## Installation and Configuration

This script use [Python client for Kuberntes](https://github.com/kubernetes-client/python). We need to install that first

```
pip install kubernetes
python K8sPurger.py
```

By default, it will run in dry-run mode and just show you the unused resources. This script is created to find the unused resource in Kubernetes and delete them. If you are sure you can delete the resources by appending flag --delete=true


```
yogesh$ python K8sPurger.py

Extra Secrets are 3 which are as below
---------------------------
| Secrets       |Namespace |
---------------------------
| appsnewsecret |apps    |
| testsecret    |apps    |
| testsecret    |default |
---------------------------
 

Extra ConfigMap are 4 which are as below
-------------------------
| ConfigMap   |Namespace |
-------------------------
| test        |apps    |
| testing     |apps    |
| test        |default |
| thisisnewcm |default |
-------------------------
 

Extra PV Claim are 1 which are as below
---------------------------
| PV Claim      |Namespace |
---------------------------
| task-pv-claim |default |
---------------------------

yogesh$ python K8sPurger.py --delete=true

This script is created to find an unused  resource in Kubernetes and delete them


Extra Secrets are 3 which are as below
---------------------------
| Secrets       |Namespace |
---------------------------
| appsnewsecret |apps    |
| testsecret    |apps    |
| testsecret    |default |
---------------------------
 

Extra ConfigMap are 4 which are as below
-------------------------
| ConfigMap   |Namespace |
-------------------------
| test        |apps    |
| testing     |apps    |
| test        |default |
| thisisnewcm |default |
-------------------------
 

Extra PV Claim are 1 which are as below
---------------------------
| PV Claim      |Namespace |
---------------------------
| task-pv-claim |default |
---------------------------
 
You have selected to delete unused items which are as above you want to continue?
Type yes or y to continue or any key to exit.
y

Deleting secretappsnewsecret....
Deleting secrettestsecret....
Deleting secrettestsecret....
Deleted All Unused Secret.

Deleting ConfigMap test....
Deleting ConfigMap testing....
Deleting ConfigMap test....
Deleting ConfigMap thisisnewcm....
Deleted All Unused ConfigMap.

Deleting PVC task-pv-claim....
Deleted All Unused PVC.

yogesh$ python K8sPurger.py --delete=true

This script is created to find unused  resource in Kubernetes and delete them

Hurrey You don't have a unused Secrets
 
Hurrey You don't have a unused ConfigMap
 
Hurrey You don't have a unused PV Claim
 
You have selected to delete unused items which are as above you want to continue?
Type yes or y to continue or any key to exit.
y
No Unused Secret to delete. Skipping deletion.
No Unused ConfigMap to delete. Skipping deletion.
No Unused Persistent volume claim to delete. Skipping deletion.
```
