#!/usr/bin/python

from kubernetes import config, client

# import argparse

UsedSecret, UsedConfigMap, UsedPVC, UsedEP, UsedSA, ExtraRoleBinding, ExtraIng, ExtraDep, ExtraSTS = [], [], [], [], [], [], [], [], []
Secrets, ConfigMap, PVC, EP, SA, = [], [], [], [], []
Ing, RoleBinding = {}, {}


def main():
    print("\nThis script is created to find unused "),
    print("resource in Kubernetes and delete them\n")
    # parser = argparse.ArgumentParser(description='Parcer to get delete value')
    # parser.add_argument('-d', '--delete', help='Input file name', required=False)
    # args = parser.parse_args()
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1beta1Api = client.ExtensionsV1beta1Api()
        RbacAuthorizationV1Api = client.RbacAuthorizationV1Api()
        AppsV1Api = client.AppsV1Api()
    except Exception as e:
        print("Not able to read Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    print("Getting unused secret it may take couple of minute..")
    GetUsedResources(v1)
    DefinedSecret(v1)
    ExtraSecret = Diffrance(Secrets, UsedSecret)
    PrintList(ExtraSecret, "Secrets")
    print("Getting unused ConfigMap it may take couple of minute..")
    DefinedConfigMap(v1)
    ExtraConfigMap = Diffrance(ConfigMap, UsedConfigMap)
    PrintList(ExtraConfigMap, "ConfigMap")
    print("Getting unused PVC it may take couple of minute..")
    DefinedPersistentVolumeClaim(v1)
    ExtraPVC = Diffrance(PVC, UsedPVC)
    PrintList(ExtraPVC, "PV Claim")
    print("Getting unused services it may take couple of minute..")
    GetUsedServices(v1)
    DefinedSvc(v1)
    ExtraSVC = Diffrance(EP, UsedEP)
    PrintList(ExtraSVC, "Services")
    print("Getting unused Ingress it may take couple of minute..")
    DefinedIngress(v1beta1Api)
    ExtraIng = GetUnusedIng(EP, ExtraSVC)
    PrintList(ExtraIng, "Ingress")
    print("Getting unused service account it may take couple of minute..")
    DefinedServiceAccount(v1)
    ExtraSA = Diffrance(SA, UsedSA)
    PrintList(ExtraSA, "Service Account")
    print("Getting unused Roles Binding it may take couple of minute..")
    DefinedRoleBinding(RbacAuthorizationV1Api)
    ExtraRB = GetUnusedRB(SA, ExtraSA)
    PrintList(ExtraRB, "Role Binding")
    GetUnusedDeployment(AppsV1Api)
    PrintList(ExtraDep, "Deployment")
    GetUnusedSTS(AppsV1Api)
    PrintList(ExtraSTS, "Stateful Sets")


def Diffrance(listA, listB):
    listC = []
    for i in listA:
        if i not in listB:
            listC.append(i)
    return listC


def PrintList(Toprint, name):
    if len(Toprint) == 0:
        print("Hurray You don't have a unused " + name)
    else:
        print("\nExtra " + name + " are " + str(len(Toprint)) + " which are as below\n")
        size1 = max(len(word[0]) for word in Toprint)
        size2 = max(len(word[1]) for word in Toprint)
        borderchar = '|'
        linechar = '-'
        # print(name + " Namespaces")
        print(linechar * (size1 + size2 + 7))
        print('{bc} {:<{}} {bc}'.format(name, size1, bc=borderchar) + '{:<{}} {bc}'.format("Namespace", size2,
                                                                                           bc=borderchar))
        print(linechar * (size1 + size2 + 7))
        for word in Toprint:
            print('{bc} {:<{}} {bc}'.format(word[0], size1, bc=borderchar) + '{:<{}} {bc}'.format(word[1], size2,
                                                                                                  bc=borderchar))
        print(linechar * (size1 + size2 + 7))
    print(" ")


def GetUsedResources(v1):
    try:
        ApiResponce = v1.list_pod_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            container = i.spec.containers
            for item in container:
                if item.env is not None:
                    for env in item.env:
                        if env.value_from is not None:
                            if env.value_from.secret_key_ref is not None:
                                UsedSecret.append(
                                    [env.value_from.secret_key_ref.name, i.metadata.namespace])
                            elif env.value_from.config_map_key_ref is not None:
                                UsedConfigMap.append(
                                    [env.value_from.config_map_key_ref.name, i.metadata.namespace])
                if item.env_from is not None:
                    for env_from in item.env_from:
                        if env_from.config_map_ref is not None:
                            UsedConfigMap.append([volume.config_map_ref.name, i.metadata.namespace])
                        elif env_from.secret_ref is not None:
                            UsedSecret.append([env_from.secret_ref.name, i.metadata.namespace])
            if i.spec.volumes is not None:
                for volume in i.spec.volumes:
                    if volume.secret is not None:
                        UsedSecret.append([volume.secret.secret_name, i.metadata.namespace])
                    elif volume.config_map is not None:
                        UsedConfigMap.append([volume.config_map.name, i.metadata.namespace])
                    elif volume.persistent_volume_claim is not None:
                        UsedPVC.append([volume.persistent_volume_claim.claim_name, i.metadata.namespace])
            if i.spec.service_account_name is not None:
                UsedSA.append([i.spec.service_account_name, i.metadata.namespace])


def DefinedSvc(v1):
    try:
        ApiResponce = v1.list_service_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            EP.append([i.metadata.name, i.metadata.namespace])


def GetUsedServices(v1):
    try:
        ApiResponce = v1.list_endpoints_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        elif i.subsets is not None:
            UsedEP.append([i.metadata.name, i.metadata.namespace])


def DefinedSecret(v1):
    try:
        ApiResponce = v1.list_secret_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        elif i.type in "kubernetes.io/tls" or i.type in "kubernetes.io/service-account-token":
            pass
        else:
            Secrets.append([i.metadata.name, i.metadata.namespace])


def DefinedConfigMap(v1):
    try:
        ApiResponce = v1.list_config_map_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            ConfigMap.append([i.metadata.name, i.metadata.namespace])


def DefinedPersistentVolumeClaim(v1):
    try:
        ApiResponce = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        PVC.append([i.metadata.name, i.metadata.namespace])


def DefinedServiceAccount(v1):
    try:
        ApiResponce = v1.list_service_account_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            SA.append([i.metadata.name, i.metadata.namespace])


def DefinedIngress(V1beta1Api):
    try:
        ApiResponce = V1beta1Api.list_ingress_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            if i.spec.rules is not None:
                for rule in i.spec.rules:
                    if rule.http.paths is not None:
                        for path in rule.http.paths:
                            Ing[i.metadata.name] = ([path.backend.service_name, i.metadata.namespace])


def GetUnusedIng(EP, ExtraSVC):
    for i, j in Ing.items():
        if j not in EP or j in ExtraSVC:
            ExtraIng.append([i, j[1]])
    return ExtraIng


def DefinedRoleBinding(RbacAuthorizationV1Api):
    try:
        ApiResponce = RbacAuthorizationV1Api.list_role_binding_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            for sub in i.subjects:
                if "ServiceAccount" in sub.kind:
                    RoleBinding[i.metadata.name] = ([sub.name, i.metadata.namespace])


def GetUnusedRB(SA, UsedSA):
    for i, j in RoleBinding.items():
        if j not in SA or j in UsedSA:
            ExtraRoleBinding.append([i, j[1]])
    return ExtraRoleBinding


def GetUnusedDeployment(AppsV1Api):
    try:
        ApiResponce = AppsV1Api.list_deployment_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            if i.spec.replicas == 0:
                ExtraDep.append([i.metadata.name, i.metadata.namespace])


def GetUnusedSTS(AppsV1Api):
    try:
        ApiResponce = AppsV1Api.list_stateful_set_for_all_namespaces(watch=False)
    except Exception as e:
        print("Not able to reach Kubernetes cluster check Kubeconfig")
        raise RuntimeError(e)
    for i in ApiResponce.items:
        if "kube-system" in i.metadata.namespace or "kube-public" in i.metadata.namespace:
            pass
        else:
            if i.spec.replicas == 0:
                ExtraSTS.append([i.metadata.name, i.metadata.namespace])


if __name__ == '__main__':
    main()
