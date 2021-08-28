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

  

## Hunt Unused Resources In Kubernetes.

### K8sPurger in action

I have created a demo video to show end to end use of K8sPurger. I have not shown monitoring setup (prometheus opertator) as there are allready lot of documentation avaliable and it would have made video very long.


[![K8sPurger](https://gifs.com/gif/k8spurger-k2rVmx)](https://www.youtube.com/watch?v=QfDvHcfCihY)

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



### Installation and Configuration

There are two ways we can run this utility. Once is ad-hoc another is deploying in Kubernetes itself which will run periodically and capture unused resources and expose them as Prometheus metrics. Once capture in Prometheus one can do all sorts of alerting and visualization. Both ways are covered in the ![Installation](./INSTALL.md) part. 

## Selection Criteria
 - Secret -> If the secret is not mounted on any running pod via env variable or as volume
 - ConfigMap -> If ConfigMap is not mounted on any running pod via env variable or as volume
 - PVC -> Is PVC is not mounted on any running pod
 - Services -> If services do not any endpoint
 - ServiceAccount -> If no running pod use that service account
 - Ingress -> If ingress pointing to any services which either do not exist or do not have any endpoint
 - RoleBinding -> If RoleBindding to any Services account which does not exist or that Services account is not used by any running pod.
 - Deployment -> If deployment have zero replica.
 - StateFullset -> If StateFullset have zero replica.


Exclusion:- All objects in kube-system and kube-system are excluded also all secrets which are token or type TLS are excluded to avoid the high list of false positive.



### NOTE:- You can browse code and if like idea provides star for encouragement or provide feedback to me one below social networks.

Twitter https://twitter.com/yogeshkunjir LinkedIn https://www.linkedin.com/in/yogeshkunjir/

<a href='https://ko-fi.com/yogeshkunjir' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee/Book at ko-fi.com' />
