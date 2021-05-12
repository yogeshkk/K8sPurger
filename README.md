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

NAQ (Nobody asked Question).

1) What this script do?

A:- This will find all unused resources and show them in a nice format and optionally remove them.

2) Why you need this?

A:- This is not required. I was learning Python and according to my Moto "Fail Fast.. Learn Faster" I started this project as we have 15+ Kubernetes clusters and we have a lot of such unused resources because of kustamize configmap/secret and a lot of POC which come and go which pile up such resources.

3) Is this cause any effect on my cluster?

A:- By default script will run in Dry-Run mode which should only get the details of the resource. There is an optional --delete=true flag if you want to delete the unused resource but it is recommended that you should run as Dry-run first to avoid any impact to the cluster. 

Note:- You should not trust strangers' words on the internet so browse the script as it is under apache 2 License and try on dummy cluster.

4) How this work? Can I just use the kubectl command to do the same?

A:- The kubectl does not directly give these details you have to invest a lot of time. If you know a short way, Please let me know via raising the issue (sharing is caring). This script will get all pods in all namespaces and scan them for these resources and make a list and then get the resource in Kubernetes and just give you the difference.

5) So if I understood correctly it will scan the pod only. what if I have deployement/StatefullSet which has zero replica set?

A:- Yes, in that case, the resource will be shown as unused. That's why this script runs in dry-run mode by default so you can see and take action yourself. If you have zero replicas mean you are not using that resource.

6) Why PVC why not PV?

A:- Normally we use PVC to manage PV and when we delete claims, PV will be deleted or retained as per storage-class configuration. To avoid any potential data loss I choose to work with PVC only.

7) What if I hit a bug or required any feature?

A:- You can raise an issue. I will try to fix the bug. The feature has to look into how much time is required.

8) I did check the script your python code is awful?

A:- Yes. As I said I am learning any guidance is welcome. You can raise PR so I can understand how PRO writes the code and improve my code.



## Installation and Configuration

This script use [Python client for Kuberntes](https://github.com/kubernetes-client/python). We need to install that first

```
pip install kubernetes
python K8sPurger.py
```

### By default, it will run in dry-run mode and just show you the unused resources such as.

```
yogesh$ python K8sPurger.py

This script is created to find unused  resource in Kubernetes and delete them

Extra Secrets are 3 which are as below
---------------------------
| Secrets       |Namespace |
---------------------------
| appsnewsecret |apps      |
| testsecret    |apps      |
| testsecret    |default   |
---------------------------
 

Extra ConfigMap are 4 which are as below
-------------------------
| ConfigMap   |Namespace |
-------------------------
| test        |apps      |
| testing     |apps      |
| test        |default   |
| thisisnewcm |default   |
-------------------------
 

Extra PV Claim are 1 which are as below
---------------------------
| PV Claim      |Namespace |
---------------------------
| task-pv-claim |default   |
---------------------------
```
### If you are sure you can delete the resources by appending flag --delete=true

```
yogesh$ python K8sPurger.py --delete=true

This script is created to find an unused  resource in Kubernetes and delete them


Extra Secrets are 3 which are as below
---------------------------
| Secrets       |Namespace |
---------------------------
| appsnewsecret |apps      |
| testsecret    |apps      |
| testsecret    |default   |
---------------------------
 

Extra ConfigMap are 4 which are as below
-------------------------
| ConfigMap   |Namespace |
-------------------------
| test        |apps      |
| testing     |apps      |
| test        |default   |
| thisisnewcm |default   |
-------------------------
 

Extra PV Claim are 1 which are as below
---------------------------
| PV Claim      |Namespace |
---------------------------
| task-pv-claim |default   |
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
```
###  You can say no even after passing --delete=true flag and script won't delete the resources.

```
yogesh$ python K8sPurger.py --delete=true

This script is created to find unused  resource in Kubernetes and delete them

Hurrey You don't have a unused Secrets
 
Hurrey You don't have a unused ConfigMap
 
Hurrey You don't have a unused PV Claim
 
You have selected to delete unused items which are as above you want to continue?
Type yes or y to continue or any key to exit.
n
You choose not to auto delete. Great choice! You can clean them up manually.
```

### NOTE:- You can browse code and if like idea provides star for encouragement or provide feedback to me one below social networks.

Twitter https://twitter.com/yogeshkunjir LinkedIn https://www.linkedin.com/in/yogeshkunjir/