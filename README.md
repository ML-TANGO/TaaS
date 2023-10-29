# TaaS (Tango As A Service)

## Docker compose to kubernetes 

### 1. Install minikube and kompose

* minikube link: https://minikube.sigs.k8s.io/docs/start/
* kompose installation link: https://kompose.io/installation/
* kompose getting started link: https://kompose.io/getting-started/

여기에서는 x86기반으로 minikube와 kompose 설치를 설명합니다.

minikube를 설치합니다.
```console
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

이후, 다음의 [kompose installation 링크](https://kompose.io/installation/) 로 kompose를 설치합니다.

여기서는 x86기반의 Linux에서 설치합니다 
```console
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
```

### 2. Run minikube

minikube와 kompose를 설치하였으면, minikube를 다음과 같이 실행합니다

```console
minikube start
```

### 3. Run kompose convert

minikube를 실행하였으면, docker-compose.yml 파일을 kubernetes에 맞게 변환 과정을 진행합니다.

변환할때 한개의 파일인 `kubernetes.yml`로 변환합니다.

```console
kompose convert -f docker-compose.yml -o kubernetes.yml
```

### 4. register k8s service

kompose를 이용하여 Docker compose(`docker-compose.yml`)에서 k8s설정파일로 변환된 `kubernetes.yml`파일을 k8s에 등록해봅니다.

```console
kubectl apply -f kubernetes.yml
```

등록이 되면, 다음의 명령어로 k8s 등록이 되었는지 확인해봅니다.

```console
$ kubectl get po -A
NAMESPACE     NAME                               READY   STATUS              RESTARTS          AGE
default       autonn-resnet-66768476f6-czm57     0/1     CrashLoopBackOff    979 (3m41s ago)   3d10h
default       autonn-yoloe-558cf9494c-tdb7n      0/1     CrashLoopBackOff    980 (73s ago)     3d10h
default       bms-5cfdd5788c-pv9z8               0/1     CrashLoopBackOff    979 (4m29s ago)   3d10h
default       cloud-deploy-79f8ccf7fd-p2ml9      1/1     Running             2 (3d10h ago)     3d10h
default       code-gen-f7b757699-c6f42           0/1     ErrImageNeverPull   0                 3d10h
default       kube-deploy-6b76b4b748-f56pk       0/1     CrashLoopBackOff    979 (62s ago)     3d10h
default       labelling-7b8bbc47bb-2jwmp         0/1     ErrImageNeverPull   0                 3d9h
default       ondevice-deploy-79c9969fcc-4hnhh   1/1     Running             2 (3d9h ago)      3d10h
default       postgresql-7df4f6c9df-dvmcr        1/1     Running             2 (3d10h ago)     3d10h
default       project-manager-88487d5b8-f5ks6    0/1     CrashLoopBackOff    980 (82s ago)     3d10h
default       registry-6d9ff564c7-p44l7          1/1     Running             2 (3d10h ago)     3d10h
default       viz2code-cb868995-z5k6r            1/1     Running             11 (3d9h ago)     3d10h
kube-system   coredns-5d78c9869d-d7lv9           1/1     Running             8 (3d10h ago)     9d
kube-system   etcd-minikube                      1/1     Running             8 (3d10h ago)     9d
kube-system   kube-apiserver-minikube            1/1     Running             8 (3d9h ago)      9d
kube-system   kube-controller-manager-minikube   1/1     Running             9 (3d10h ago)     9d
kube-system   kube-proxy-xmfs7                   1/1     Running             8 (3d10h ago)     9d
kube-system   kube-scheduler-minikube            1/1     Running             8 (3d10h ago)     9d
kube-system   storage-provisioner                1/1     Running             15 (3d9h ago)     9d
```

### 5. After converted kompose

Docker Compose 설정파일 `docker-compose.yml`을 Kubernetes 설정파일인 `kubernetes.yml`파일로 변환 후에 추가로 해줘야 할 작업이 있습니다.

#### 누락된 서비스 등록

docker-compose.yml파일을 kompose로 k8s 구동가능한 형태로 변환하다보면, postgresql service가 누락되는 경우가 있습니다.

서비스 확인은 다음의 명령어로 확인 가능합니다.
```console
kubectl get services
```

이 경우에 대해서, 변환된 kubernetes.yml파일에 postgresql service를 추가하면 됩니다. 

postgresql의 5432 포트등록 후, `kubernetes.yml`파일을 다시 적용후 서비스 확인을 해봅니다 

아래는 `kubernetes.yml`파일에 추가한 서비스 설정 내용입니다.
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
spec:
  ports:
    - name: postgresql
      port: 5432
      targetPort: 5432
  selector:
    io.kompose.service: postgresql
status:
  loadBalancer: {}

---
```

`kubernetes.yml`파일 수정이 완료되었으면, k8s에 설정 적용해봅니다.

```console
kubectl apply -f kubernetes.yml
```


서비스 추가후, 서비스 등록 확인해보면 postgresql이 등록됨을 확인할 수 있습니다
```console
$ kubectl get service
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
autonn-resnet     ClusterIP   10.103.113.185   <none>        8092/TCP                     9d
autonn-yoloe      ClusterIP   10.107.200.4     <none>        8090/TCP                     9d
bms               ClusterIP   10.99.158.245    <none>        8081/TCP                     9d
cloud-deploy      ClusterIP   10.111.8.6       <none>        7007/TCP,8080/TCP,8890/TCP   9d
code-gen          ClusterIP   10.104.190.185   <none>        8888/TCP                     9d
kube-deploy       ClusterIP   10.105.88.193    <none>        8901/TCP                     9d
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP                      9d
labelling         ClusterIP   10.110.199.100   <none>        8086/TCP,8095/TCP            9d
ondevice-deploy   ClusterIP   10.103.52.253    <none>        8891/TCP                     9d
postgresql        ClusterIP   10.111.25.236    <none>        5432/TCP                     3d10h
project-manager   ClusterIP   10.107.115.139   <none>        8085/TCP                     9d
registry          ClusterIP   10.108.17.170    <none>        8903/TCP                     9d
viz2code          ClusterIP   10.109.11.0      <none>        8091/TCP                     9d
```


#### Docker local image 설정 추가 및 태그 추가

kubernetes.yml파일에서 Docker 이미지를 local에서 제대로 불러들이지 못하는 경우가 있습니다. 

```console
$ kubectl get po -A
```
로 서비스 조회시 `ImagePullBackOff`가 나오는 경우가 있습니다.

이 경우 Docker local image를 불러올 수 있게 yml파일을 추가합니다.

예를 들어, `imagePullPolicy: Never` 항목을 다음의 예처럼 추가하면 됩니다.

```
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    metadata:
    spec:
      containers:
        - args:
            - sh
            - -c
            - cd /app && python3 code_gen.py
          image: code-gen
          imagePullPolicy: Never
          name: code-gen
          ports:
            - containerPort: 8888
              hostPort: 8888
              protocol: TCP
          resources: {}
```

이후, `kubernetes.yml`파일 수정이 완료되었으면, k8s에 설정 적용해봅니다.

```console
kubectl apply -f kubernetes.yml
```


##### kubernetes pod의 로그 조회하기 

만약, kubernetes pod 가 제대로 실행이 되지 않을때, 로그를 조회하면 어디가 문제가 있는지 확인 가능합니다.

로그 조회를 위해 kubernetes pod 이름을 조회해봅니다.
```console
$ kubectl get po -A
NAMESPACE              NAME                                         READY   STATUS              RESTARTS          AGE
default                autonn-resnet-66768476f6-czm57               0/1     CrashLoopBackOff    986 (60s ago)     3d11h
default                autonn-yoloe-558cf9494c-tdb7n                0/1     CrashLoopBackOff    986 (3m43s ago)   3d11h
default                bms-5cfdd5788c-pv9z8                         0/1     CrashLoopBackOff    986 (104s ago)    3d11h
default                cloud-deploy-79f8ccf7fd-p2ml9                1/1     Running             2 (3d10h ago)     3d11h
default                code-gen-f7b757699-c6f42                     1/1     Running             0                 3d11h
default                kube-deploy-6b76b4b748-f56pk                 0/1     CrashLoopBackOff    985 (3m29s ago)   3d11h
default                labelling-7b8bbc47bb-2jwmp                   0/1     ErrImageNeverPull   0                 3d10h
default                ondevice-deploy-79c9969fcc-4hnhh             1/1     Running             2 (3d10h ago)     3d11h
default                postgresql-7df4f6c9df-dvmcr                  1/1     Running             2 (3d10h ago)     3d11h
default                project-manager-88487d5b8-f5ks6              0/1     CrashLoopBackOff    986 (3m54s ago)   3d11h
default                registry-6d9ff564c7-p44l7                    1/1     Running             2 (3d10h ago)     3d11h
default                viz2code-cb868995-z5k6r                      1/1     Running             11 (3d10h ago)    3d11h
kube-system            coredns-5d78c9869d-d7lv9                     1/1     Running             8 (3d10h ago)     9d
kube-system            etcd-minikube                                1/1     Running             8 (3d10h ago)     9d
kube-system            kube-apiserver-minikube                      1/1     Running             8 (3d10h ago)     9d
kube-system            kube-controller-manager-minikube             1/1     Running             9 (3d10h ago)     9d
kube-system            kube-proxy-xmfs7                             1/1     Running             8 (3d10h ago)     9d
kube-system            kube-scheduler-minikube                      1/1     Running             8 (3d10h ago)     9d
kube-system            metrics-server-7746886d4f-nn9wb              1/1     Running             0                 30m
kube-system            storage-provisioner                          1/1     Running             15 (3d10h ago)    9d
kubernetes-dashboard   dashboard-metrics-scraper-5dd9cbfd69-lzqx2   1/1     Running             0                 32m
kubernetes-dashboard   kubernetes-dashboard-5c5cfc8747-mss9m        1/1     Running             0                 32m
```

여기서 에러가 난 pod은 `Running`상태가 아닌 `CrashLoopBackOff`, `Error`, `ErrImageNeverPull`, `ImagePullBackOff`등이 나옵니다.

구체적인 에러 조회를 위해서는 pod의 NAME을 얻은 후, pod 실행 로그를 조회합니다

```console
$ kubectl logs project-manager-88487d5b8-f5ks6
chmod: cannot access './wait_for_postgres.sh': No such file or directory
```

pod 실행 로그에서 확실한 내용을 확인할 수 없으면 
이미지 실행시 어디에 이슈 있는지 상세 내역을 다음과 같이 조회할 수 있습니다.

```console
$ kubectl describe pod project-manager
Name:             project-manager-88487d5b8-f5ks6
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 25 Oct 2023 23:06:59 +0900
Labels:           io.kompose.network/tango-default=true
                  io.kompose.service=project-manager
                  pod-template-hash=88487d5b8
Annotations:      kompose.cmd: kompose convert -f docker-compose.yml -o kubernetes.yml
                  kompose.version: 1.31.2 (a92241f79)
Status:           Running
IP:               10.244.0.190
IPs:
  IP:           10.244.0.190
Controlled By:  ReplicaSet/project-manager-88487d5b8
Containers:
  project-manager:
    Container ID:  docker://bc9d351f0df692d5f0c210bd76492ce0959bdc11af1ad43ce2af6e99a38ad8ea
    Image:         project-manager
    Image ID:      docker://sha256:8a40555ff92cc16a2279d2ff6c102d894d955ba04ee9e6119c3a1983f7dafe6c
    Port:          8085/TCP
    Host Port:     8085/TCP
    Args:
      sh
      -c
      chmod 777 ./wait_for_postgres.sh &&
             ./wait_for_postgres.sh &&
             python manage.py makemigrations tango &&
             python manage.py migrate &&
             python manage.py collectstatic --no-input &&
             python manage.py loaddata base_model_data.json &&
             python manage.py runserver 0.0.0.0:8085
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Sun, 29 Oct 2023 10:52:21 +0900
      Finished:     Sun, 29 Oct 2023 10:52:21 +0900
    Ready:          False
    Restart Count:  994
    Environment:
      POSTGRES_NAME:      postgres
      POSTGRES_PASSWORD:  postgres
      POSTGRES_USER:      postgres
    Mounts:
      /code from project-manager-claim0 (rw)
      /shared from shared (rw)
      /var/run/docker.sock from project-manager-claim2 (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-6nrsc (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
  PodScheduled      True
Volumes:
  project-manager-claim0:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  project-manager-claim0
    ReadOnly:   false
  shared:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  shared
    ReadOnly:   false
  project-manager-claim2:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  project-manager-claim2
    ReadOnly:   false
  kube-api-access-6nrsc:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason   Age                        From     Message
  ----     ------   ----                       ----     -------
  Warning  BackOff  2m49s (x23055 over 3d11h)  kubelet  Back-off restarting failed container project-manager in pod project-manager-88487d5b8-f5ks6_default(1cf91943-fc85-4a46-9af4-eb92edfc6581)

```


##### k8s 조회할 수 있게 docker 빌드하기 

docker-compose.yml파일에 위치한 Dockerfile 경로를 조회합니다

이후, 다음과 같이 환경설정을 합니다.
```console
 eval $(minikube -p minikube docker-env)
```

이후, Docker 빌드합니다
```
~/TANGO/deploy_codegen/optimize_codegen$ docker build -t tango_code_gen:latest .
```

빌드 후 태그를 추가합니다
```
docker tag tango_code_gen:latest code-gen
```

이후, k8s에 설정 적용해봅니다.

```console
kubectl apply -f kubernetes.yml
```
다음에 kubernetes pod 이 정상으로 돌아가는지 조회하면 됩니다.
```console
kubectl get po -A
```