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

  

## A Simple script to hunt unused Kubernetes resources.

  

### Release History

Release 0.3 

 - Added Ingress
 - Added Services Account
 - Adding RoleBindding
 - Removed deletion capability. [Refer issue 3](https://github.com/yogeshkk/K8sPurger/issues/3)

Release 0.2
 - Added services in the mix.

  

### NAQ (Nobody asked Question).

  

1) What this script do?
> This will find all unused resources and show them in a nice format.

2) Why you need this?
>When we add a new application or Microservices it is simple as installing a chart or kubectl -f on a big manifest but when we want to remove we don't know what are resources it created. Many times we can't remove them fully because we have 10's or 100's such resources and don’t have enough time to hunt and kill or many times we just inherited a cluster. Having an unused item in the cluster is not good practice as the Etcd DB size grows the performance starts degrading. Also many times it possed a security risk(unknown SA and rolebinding). 

>Lastly most dear to us saving cost in case of PVC we are paying for them to cloud provider.


3) Is this cause any effect on my cluster?
>This will just list the unused resources according to predefined criteria which are mentioned after NAQ. This will just give the list of resources that are **Potentially** unused so you can focus on them an only instant of looking for a needle in the haystack.

>*Note:- You should not trust strangers' words on the internet so browse the script as it is under apache 2 License and try on dummy cluster.*

4) How this work? Can I just use the kubectl command to do the same?
> The kubectl does not directly give these details you have to invest a lot of time. If you know a short way, Please let me know via raising the issue (sharing is caring). This script will get all pods in all namespaces and scan them for these resources and make a list and then get the resource in Kubernetes and just give you the difference. 

5) So if I understood correctly it will scan the pod only. what if I have deployment/StatefullSet which has zero replica set?
> Yes, in that case, the resource will be shown as unused. If you have zero replicas means you are not using that resource.

6) Why PVC why not PV?
> Normally we use PVC to manage PV and when we delete claims, PV will be deleted or retained as per storage-class configuration. To avoid any potential data loss I choose to work with PVC only.  

8) What if I hit a bug or required any feature?
> You can raise an issue. I will try to fix the bug. The feature has to look into how much time is required.


### Selection Criteria
 - Secret -> If the secret is not mounted on any running pod via env variable or as volume
 - ConfigMap -> If ConfigMap is not mounted on any running pod via env variable or as volume
 - PVC -> Is PVC is not mounted on any running pod
 - Services -> If services do not any endpoint
 - ServiceAccount -> If no running pod use that service account
 - Ingress -> If ingress pointing to any services which either do not exist or do not have any endpoint
 - RoleBinding -> If RoleBindding to any Services account which does not exist or that Services account is not used by any running pod.

Exclusion:- All objects in kube-system and kube-system are excluded also all secrets which are token or type TLS are excluded to avoid the high list of false positive.


## Installation and Configuration

  

This script use [Python client for Kuberntes](https://github.com/kubernetes-client/python). We need to install that first

  

```

pip install kubernetes

python K8sPurger.py

```


### Make sure you have kubeconfig in ~/.kube/conf or in KUBECONFIG env variable before runing script.

  

```

yogesh$ ~/p/K8sPurger> python K8sPurger.py

This script is created to find unused resource in Kubernetes.

Getting unused secret it may take couple of minute..

Extra Secrets are 6 which are as below

--------------------------------
| Secrets         | Namespace   |
--------------------------------
| app1-secret     | my-apps     |
| app2-secret     | my-apps     |
| app2-new-secret | my-apps     |
| postgresql      | default     |
| dex-b94455424g  | kube-addons |
| dex-dbh8fmk699  | kube-addons |
--------------------------------

Getting unused ConfigMap it may take couple of minute..

Extra ConfigMap are 6 which are as below

-------------------------------------------
| ConfigMap                 | Namespace   |
-------------------------------------------
| app1-configmap            | my-apps     |
| app2-configmap            | my-apps     |
| app2-new-configmap        | my-apps     |
| ss-cm                     | default     |
| cluster-autoscaler-status | kube-addons |
| fluent-bit-config         | logging     |
-------------------------------------------

Getting unused PVC it may take couple of minute..

Extra PV Claim are 5 which are as below
---------------------------------
| PV Claim          | Namespace |
---------------------------------
| data-postgresql-0 | default   |
| data-0            | default   |
| redis-master-0    | default   |
| redis-slave-0     | default   |
| redis-slave-1     | default   |
--------------------------------

Getting unused services it may take couple of minute..

Extra Services are 3 which are as below

-----------------------------
| Services      | Namespace |
-----------------------------
| app1-services | my-apps   |
| app2-services | my-apps   |
| app2-headless | my-apps   |
-----------------------------

Getting unused Ingress it may take couple of minute..

Extra Ingress are 4 which are as below

----------------------------------------
| Ingress                  | Namespace |
----------------------------------------
| app1-ingress             | my-apps   |
| app2-ingress             | my-apps   |
| app2-ingress-api-gateway | my-apps   |
| router                   |default    |
----------------------------------------

Getting unused service account it may take couple of minute..

Extra Service Account are 6 which are as below
----------------------------------
| Service Account | Namespace    |
----------------------------------
| app1-svc        | my-apps      |
| cert-svc        | cert-manager |
| log-svc         | logging      |
| monitor-svc     | monitoring   |
| default         | my-registry  |
| default         | tools        |
----------------------------------

Getting unused Roles Binding it may take couple of minute..

Extra Role Binding are 1 which are as below

---------------------------
| Role Binding |Namespace |
---------------------------
| app1-rb      |my-apps   |
---------------------------

```

  

### NOTE:- You can browse code and if like idea provides star for encouragement or provide feedback to me one below social networks.

Twitter https://twitter.com/yogeshkunjir LinkedIn https://www.linkedin.com/in/yogeshkunjir/