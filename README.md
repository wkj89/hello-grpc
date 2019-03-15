### demo主要用意
 1. demo注意示例如何创建grpc的service 跟client
 2. 如何使用istio创建流量网关与流量控制
 3. spinnaker发布
 4. k8s的命令行工具使用
 5. filebeat的自动注入，日志推送ELK
 
### init
 1. spinnaker 已经有我部署好的client跟service  可以直接看配置
 2. 如需自己体验发布，可以自行修改代码，build，创建全新的service跟pipline
 3. 或者删除原有的land balance 跟service group  
 


### 安装k8s相关命令行工具
1. brew install awscli (已安装aws python包可忽略）
2.【aws官方教程](https://docs.aws.amazon.com/zh_cn/eks/latest/userguide/getting-started.html) 参照《为 Amazon EKS 安装和配置 kubectl》部分安装kubectl，aws-iam-authenticator
3. aws eks --region us-west-2 update-kubeconfig --name shoppo-dev
4. kubectl get node
 ```
 NAME                                       STATUS    ROLES     AGE       VERSION
ip-10-0-1-84.us-west-2.compute.internal    Ready     <none>    4d        v1.10.3
ip-10-0-2-193.us-west-2.compute.internal   Ready     <none>    4d        v1.10.3
ip-10-0-5-45.us-west-2.compute.internal    Ready     <none>    4d        v1.10.3

 ```
 如显示类似信息表示一切正常


### build docker 镜像


### 部署grpc-service
 1. 使用test的application
 2. 创建LB
   - Stack 为你service的name，假设为greeter，那么对外服务的地址为test-greeter
   - port targetport 为50051 ，name为grpc
   - Advanced Settings 的Type 为clusterIP
 3. 创建pipline

   - Automated Triggers
     - 选择docker registry
     - Registry Name ：aws
   - add stage
     - Type: deploy
   - add service group
     - stack： greeter
     - Strategy: highland
     - Containers: 选择hello-grpc
     - load balance： test-greeter
   - Replicas
     - Autoscaling：勾选
     - Max：4
     - Desired：2
   - Advanced Settings
     - Pod Annotations
        - key: injector.tumblr.com/request  value :log-inject
   - Container
     - Environment Variables
        - key: $service value: grpc
     - Ports
        - Container Port:50051
        - name:grpc




### 部署web
 1. 使用test的application
 2. 创建LB
   - Stack 为你service的name，假设为web，那么对外服务的地址为test-web
   - port 80  targetport 4000
   - Advanced Settings 的Type 为clusterIP
 3. 创建pipline
   - Automated Triggers
     - 选择docker registry
     - Registry Name ：aws
   - add stage
     - Type: deploy
   - add service group
     - stack： web
     - Strategy: highland
     - Containers: 选择hello-grpc
     - load balance： test-web
      - Advanced Settings
   - Pod Annotations
        - key: injector.tumblr.com/request  value :log-inject      # 使用webhook注入filebeat镜像
   - Container
     - Environment Variables
        - Name: service value: web  Source:explict
     - Ports
        - Container Port:4000
     - probes
       - Readiness Probe
           - port：4000
           - Path /live
       - Liveness Probe
           - 同上

### 发布
  1. 发布刚刚设定的2个pipline
  2. kubectl create -f istio-gateway.yaml

### 测试

 1. 浏览器打开：http://istio-dev.shoppo.com/shoppo
 2. 注意每次返回的hostname不一样


