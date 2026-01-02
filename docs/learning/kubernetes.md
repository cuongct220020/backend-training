# Kubernetes: Từ Docker Compose đến quản lý microservices chuyên nghiệp


## Mục lục

[Giới thiệu: Vượt qua giới hạn của Docker](#giới-thiệu-vượt-qua-giới-hạn-của-docker)

[Phần 1. Bước nhảy vọt về tư duy - từ Docker Compose đến điều phối](#phần-1-bước-nhảy-vọt-về-tư-duy---từ-docker-compose-đến-điều-phối)
* [1.1. Từ "vật cưng" (pets) đến "gia súc" (cattle)](#11-từ-vật-cưng-pets-đến-gia-súc-cattle)
* [1.2. Điều phối Container (Container Orchestration) là gì?](#12-điều-phối-container-container-orchestration-là-gì)

[Phần 2. Kiến trúc tổng quan của Kubernetes (K8s 101)](#phần-2-kiến-trúc-tổng-quan-của-kubernetes-k8s-101)
* [2.1. Control Plane: Bộ não của Cụm](#21-control-plane-bộ-não-của-cụm)
* [2.2. Worker Nodes: Cơ bắp của Cụm](#22-worker-nodes-cơ-bắp-của-cụm)

[Phần 3. Các khái niệm cốt lõi trong ứng dụng stateless](#phần-3-các-khái-niệm-cốt-lõi-trong-ứng-dụng-stateless)
* [3.1. Khái niệm `Pod`: Đơn vị triển khai nhỏ nhất](#31-khái-niệm-pod-đơn-vị-triển-khai-nhỏ-nhất)
* [3.2. Khái niệm `Deployment`: Quản lý vòng đời ứng dụng tateless](#32-khái-niệm-deployment-quản-lý-vòng-đời-ứng-dụng-tateless)
* [3.3. Khái niệm `Service`: Kết nối các Microservices với nhau](#33-khái-niệm-service-kết-nối-các-microservices-với-nhau)

[Phần 4. Quản lý cấu hình và dữ liệu bền vững](#phần-4-quản-lý-cấu-hình-và-dữ-liệu-bền-vững)
* [4.1. `ConfigMap`: Tiêm cấu hình (Không nhạy cảm)](#41-configmap-tiêm-cấu-hình-không-nhạy-cảm)
* [4.2. `Secret`: Quản lý dữ liệu Nhạy cảm](#42-secret-quản-lý-dữ-liệu-nhạy-cảm)
* [4.3. Quản lý lưu trữ bền vững `PersistentVolume` (PV) và `PersistentVolumeClaim` (PVC)](#43-quản-lý-lưu-trữ-bền-vững-persistentvolume-pv-và-persistentvolumeclaim-pvc)

[Phần 5. Quản lý ứng dụng Stateful - Bài toán Database và Message Queue](#phần-5-quản-lý-ứng-dụng-stateful---bài-toán-database-và-message-queue)
* [5.1. Tại sao `Deployment` không đủ cho Database](#51-tại-sao-deployment-không-đủ-cho-database)
* [5.2. Giới thiệu `StatefulSet`: "Deployment" cho ứng dụng Stateful](#52-giới-thiệu-statefulset-deployment-cho-ứng-dụng-stateful)
* [5.3. `Headless Service`: DNS cho `StatefulSet`](#53-headless-service-dns-cho-statefulset)

[Phần 6. Đưa ứng dụng ra ngoài - quản lý truy cập với Ingress](#phần-6-đưa-ứng-dụng-ra-ngoài---quản-lý-truy-cập-với-ingress)
* [6.1. Vấn đề của `Service type: LoadBalancer`](#61-vấn-đề-của-service-type-loadbalancer)
* [6.2. Giới thiệu `Ingress`: Bộ định tuyến](#62-giới-thiệu-ingress-bộ-định-tuyến)
* [6.3. Kiến trúc 2 thành phần: `Ingress` và `Ingress Controller`](#63-kiến-trúc-2-thành-phần-ingress-và-ingress-controller)

[Phần 7. Lộ trình thực hành - "Hands on" với Kubernetes](#phần-7-lộ-trình-thực-hành---hands-on-với-kubernetes)
* [7.1. Thiết lập môi trường phát triển (local development)](#71-thiết-lập-môi-trường-phát-triển-local-development)
* [7.2. Làm chủ `kubectl`: Giao tiếp với Cluster](#72-làm-chủ-kubectl-giao-tiếp-với-cluster)

[Phần 8. Đưa vào Production - Hoàn thiện hệ thống Microservices](#phần-8-đưa-vào-production---hoàn-thiện-hệ-thống-microservices)
* [8.1. Quản lý gói ứng dụng với `Helm`](#81-quản-lý-gói-ứng-dụng-với-helm)
* [8.2. Giám sát (Monitoring): Kiến trúc Prometheous & Grafana](#82-giám-sát-monitoring-kiến-trúc-prometheous--grafana)
* [8.3. Thu thập Logs: Cuộc chiến của EFK và Loki](#83-thu-thập-logs-cuộc-chiến-của-efk-và-loki)
* [8.4. Bảo mật cơ bản: `RBAC` (Role-Based Access Control)](#84-bảo-mật-cơ-bản-rbac-role-based-access-control)

[Phần 9. Cấp độ chuyên gia - Quản lý giao tiếp nâng cao với Service Mesh](#phần-9-cấp-độ-chuyên-gia---quản-lý-giao-tiếp-nâng-cao-với-service-mesh)
* [9.1. Khi nào Kubernetes Networking là đủ?](#91-khi-nào-kubernetes-networking-là-đủ-)
* [9.2. `Service Mesh` là gì?](#92-service-mesh-là-gì-)
* [9.3. Kiến trúc `Sidecar Proxy`](#93-kiến-trúc-sidecar-proxy)
* [9.4. So sánh Istio và Linkerd](#94-so-sánh-istio-và-linkerd)

[Phần 10. Tổng kết lộ trình và các bước tiếp theo](#phần-10-tổng-kết-lộ-trình-và-các-bước-tiếp-theo-)
* [10.1. Tóm tắt lộ trình của bạn](#101-tóm-tắt-lộ-trình-của-bạn)
* [10.2. Các chủ đề nâng cao tự nghiên cứu](#102-các-chủ-đề-nâng-cao-tự-nghiên-cứu)


## Giới thiệu: Vượt qua giới hạn của Docker

Hiện tại Docker Compose là công cụ tuyệt vời để định nghĩa và chạy các ứng dụng đa container trên một máy chủ duy nhất. 
Tuy nhiên, khi xây dựng một hệ thống microservices thực thụ cho môi trường production, 
bạn sẽ nhanh chóng đối mặt với những thách thức mà Docker Compose không được thiết kế để giải quyết. 
* **Khả năng mở rộng (Scalability):** Làm thế nào để mở rộng quy mô một service từ 1 lên 100 container và cân bằng tải giữa chúng? Docker Compose chỉ có thể scale thủ công trên một host.   
* **Tính sẵn sàng cao (High Availability):** Điều gì xảy ra khi máy chủ (host) chạy Docker Compose gặp sự cố? Toàn bộ hệ thống sẽ sập. 
* **Tự phục hồi (Self-healing):** Nếu một container bị "crash" (lỗi), ai sẽ khởi động lại nó? Docker Compose không có cơ chế tự động phục hồi tinh vi. 
* **Mạng (Networking):** Làm thế nào để các container trên nhiều máy chủ khác nhau nói chuyện với nhau một cách an toàn và hiệu quả?

Đây chính là lúc Kubernetes (K8s) xuất hiện. K8s không chỉ là một "công cụ quản lý container"; nó là một **nền tảng điều phối container (Container Orchestration Platform).** 
Nó cung cấp một bộ khung tự động hoá mạnh mẽ để triển khai, mở rộng quy mô, và quản lý các ứng dụng container hoá trên một cum (cluster) gồm nhiều máy chủ.
Lộ trình này sẽ trang bị cho bạn kiến thức từ kiến trúc cốt lõi đến các kỹ thuật vận hành nâng cao để sử dụng K8s một cách hiệu quả. 

## Phần 1. Bước nhảy vọt về tư duy - Từ Docker Compose đến Điều phối

Để bắt đầu, chúng ta cần thay đổi một mô hình tư duy (mental model) cơ bản.

### 1.1. Từ "Vật cưng" (Pets) đến "Gia súc" (Cattle)
Với Docker Compose trên một máy chủ, bạn có xu hướng đối xử với các container của mình như những "vật cưng" (Pets). 
Nếu một container "bệnh" (bị lỗi), bạn sẽ đăng nhập thủ công, kiểm tra (debug), và "chữa trị" cho nó. Mỗi container là duy nhất và không thể thiếu.

Kubernetes giới thiệu một triết lý hoàn toàn khác: "gia súc" (Cattle). Trong một hệ thống lớn, các container được xem là giống hệt nhau, 
không tên tuổi và dễ dàng bị thay thế. Nếu một container "bệnh", Kubernetes không cố gắng "chữa" nó; nó chỉ đơn giản là "giết" container đó và tạo ra một container mới, khỏe mạnh để thay thế. 

Triết lý này là nền tảng cho siêu năng lục của Kubernetes:
* **Tự phục hồi (self-healing):** K8s liên tục theo dõi trạng thái của các container. Nếu một container hoặc thậm chí cả một node (máy chủ) chết, 
K8s sẽ tự động khởi động lại hoặc lên lịch  (reschedule) các container đó trên các node khoẻ mạnh khác để đảm bảo trạng thái mong muốn luôn được duy trì. 
* **Tự động mở rộng (auto-scaling):** K8s có thể tự động tăng hoặc giảm số lượng container (Pods) dựa trên các chỉ số như CPU. RAM (Horizontal Pod Autoscaler - HPA). 
Nó thậm chí có thể tự động thêm hoặc bớt máy chủ (Nodes) vào cụm (Cluster Autoscaler).
* **Khám phá dịch vụ (Service Discovery):** Bạn không cần "hardcode" địa chỉ IP. K8s cung cấp một hệ thống DNS nội bộ, cho phép microservices tìm thấy nhau qua tên dịch vụ một cách ổn định. 

### 1.2. Điều phối container (Container Orchestration) là gì? 
Điều phối container là quá trình tự động hoá việc quản lý vòng đời của các ứng dụng container hoá. Nó tự động hoá các tác vụ lặp đi lặp lại và tốn thời gian như tạo, thay đổi quy mô, 
và nâng cấp container, giải phóng các lập trình viên khỏi công việc thủ công. K8s cung cấp khả năng kiểm soát chi tiết về số lượng phiên bản ứng dụng chạy đồng thời, 
cho phép điều chỉnh quy mô linh hoạt theo nhu cầu và tải công việc. 

Docker Compose là một công cụ tuyệt vời cho môi trường development và các ứng dụng nhỏ trên một host. Kubernetes được thiết kế cho các hệ thống phân tán, quy mô lớn, sẵn sàng cho production, đặc biệt là các kiến trúc microservices. 
Rất may, bạn không cần phải chọn một trong hai; nhiều nhóm DevOps sử dụng cả hai: Docker Compose cho local development và Kubernetes cho production.

## Phần 2. Kiến trúc Tổng quan của Kubernetes (K8s 101)

Một cụm Kubernestes (Kubernetes Cluster) bao gồm hai loại máy chủ chính: **Control Plane** (trước đây gọi là Master) và **Worker Nodes**. 

### 2.1. Control Plane: Bộ não của Cụm
Control Plane là trung tâm điều khiển, ra quyết định và lưu trữ trạng thái của cụm. Nó bao gồm các thành phần sau:
* `etcd`: Đây là "bộ não" thực sự, một kho lưu trữ key-value phân tán, nhất quán và có độ sẵn sàng cao. `etcd` lưu trữ toàn bộ trạng thái của cụm (bao gồm cấu hình, trạng thái của Pods, Services,v.v.). 
Đây là nguồn chân lý (single source of truth) duy nhất của K8s.  
* `kube-apiserver`: Đây là "cửa ngõ" (frontend) của Control Plane. Mọi tương tác với cụm K8s (từ người dùng, `kubectl`, hoặc các thành phần khác) đều phải đi qua API Server. API Server xác thực yêu cầu, 
sau đó đọc/ghi trạng thái vào `etcd`.
* `kube-scheduler`: Thành phần này "theo dõi" API Server để tìm các Pods mới được tạo nhưng chưa được gán cho máy chủ. Nhiệm vụ của nó là tìm một worker node phù hợp nhất (dựa trên tài nguyên, constraints) cho Pod đó.
* `kube-controller-manager`: Đây là một tập hợp các "bộ điều khiển" (controllers) chạy trong một quy trình duy nhất. Mỗi controller chạy một "vòng lặp đối chiếu" (reconcilliation loop): nó so sánh trạng thái 
mong muốn (desired state, lưu trong `etcd`) với trạng thái thực tế (actual state) của cụm và thực hiện hành động để đưa thực tế về khớp với mong muốn. Ví dụ: `Replication Controller` đảm bảo số lượng Pod mong muốn luôn chạy. 

Khi bạn (người dùng) gửi một file YAML (ví dụ: "tôi muốn chạy 3 bản sao NGINX") bằng lệnh `kubectl apply`, bạn đang nói chuyện với `kube-apiserver`. `apiserver` lưu "trạng thái mong muốn" này vào `etcd`.
`kube-controller-manager` phát hiện sự khác biệt ("mong muốn 3, thực tế 0") và tạo ra 3 Pod. 
`kube-scheduler` thấy 3 Pod này, tìm Node cho chúng và cập nhật trạng thái. Quá trình này được gọi là **mô hình khai báo (declarative model).**

### 2.2. Worker Nodes: Cơ bắp của cụm
Worker Nodes là các máy chủ (vật lý hoặc ảo) thực sự làm công việc: chạy các container ứng dụng của bạn. Mỗi Worker Node chạy các thành phần sau:
* **kubelet:** Là một "agent" (Đại lý) chạy trên mỗi node. Nó giao tiếp với `kube-apiserver`, nhận chỉ thị (ví dụ: "hãy chạy Pod X trên Node của anh") và đảm bảo các container trong Pod đó đang chạy và khỏe mạnh. 
Nó cũng báo cáo trạng thái của Node và Pods về cho Control Plane.
* **kube-proxy:** Là một network proxy chạy trên mỗi Node. Nó duy trì các quy tắc mạng (network rules) trên Node (thường là sử dụng `iptables`). 
`kube-proxy` chính là thành phần "ma thuật" làm cho các service hoạt động; nó bắt (intercept) traffic được gửi đến IP ảo của `Service` và chuyển hướng (route) đén một Pod thực tế.
* **Container Runtime:** Đây là phần mềm chịu trách nhiệm chạy container. Mặc dù Docker là phổ biến, K8s sử dụng một API trừu tượng gọi là CRI (Container Runtime Interface). 
Điều này có nghĩa là K8s có thể chạy với nhiều runtime khác nhau `containerd` (cốt lõi của Docker) hoặc `CRI-O`. Gần đây, K8s đã loại bỏ `dockershim` (lớp trung gian để tương thích với Docker) 
để ủng hộ các runtime tuân thủ CRI trực tiếp. 

Dưới đây là bảng tóm tắt kiến trúc K8s:

**Bảng 1: Các thành phần chính của Kubernetes Cluster**
<table>
  <thead>
    <tr>
      <th>Thành phần</th>
      <th>Vị trí</th>
      <th>Vai trò chính</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="3"><strong>Control Plane (Não)</strong></td>
    </tr>
    <tr>
      <td><code>etcd</code></td>
      <td>Control Plane</td>
      <td>Lưu trữ trạng thái (database) của toàn bộ cụm.</td>
    </tr>
    <tr>
      <td><code>kube-apiserver</code></td>
      <td>Control Plane</td>
      <td>Cổng giao tiếp (API) duy nhất, xác thực và ghi vào <code>etcd</code>.</td>
    </tr>
    <tr>
      <td><code>kube-scheduler</code></td>
      <td>Control Plane</td>
      <td>Quyết định Pod sẽ chạy trên Node nào.</td>
    </tr>
    <tr>
      <td><code>kube-controller-manager</code></td>
      <td>Control Plane</td>
      <td>Chạy các vòng lặp để đưa trạng thái thực tế về trạng thái mong muốn.</td>
    </tr>
    <tr>
      <td colspan="3"><strong>Worker Nodes (Cơ bắp)</strong></td>
    </tr>
    <tr>
      <td><code>kubelet</code></td>
      <td>Mọi Node (Worker)</td>
      <td>Agent trên Node, nhận lệnh từ <code>apiserver</code> và quản lý vòng đời Pod.</td>
    </tr>
    <tr>
      <td><code>kube-proxy</code></td>
      <td>Mọi Node (Worker)</td>
      <td>Quản lý mạng (iptables) cho <code>Service</code>, cho phép giao tiếp.</td>
    </tr>
    <tr>
      <td>Container Runtime</td>
      <td>Mọi Node (Worker)</td>
      <td>Phần mềm thực thi (chạy) container (ví dụ: <code>containerd</code>).</td>
    </tr>
  </tbody>
</table>

## Phần 3. Các khái niệm cốt lõi cho ứng dụng Stateless
Giờ đây, chúng ta sẽ tìm hiểu các "khối lego" cơ bản nhất bạn dùng để xây dựng ứng dụng.

### 3.1. Khái niệm `Pod`: Đơn vị triển khai nhỏ nhất
Đây là khái niệm cơ bản nhất mà người dùng Docker hay nhầm lẫn. 
* `Pod` không phải là một container. 
* `Pod` là một đơn vị công việc (workload) nhỏ nhất, cơ bản trong K8s. 
* Một `Pod` là một nhóm gồm một hoặc nhiều container (ví dụ: container ứng dụng chính và một container `sidecar` để logging).
* Các container bên trong một `Pod` **chia sẻ chung** không gian mạng (network namespaces - chúng có thể nói chuyện với nhau qua `localhost`), 
chung IP, và chung bộ lưu trữ (volumes). 

Mô hình `Pod` cho phép K8s quản lý các ứng dụng phụ trợ (như sidecar) một cách linh hoạt mà không cần gộp chúng vào container chính. 

Ví dụ YAML: Một `Pod` Nginx cơ bản. 
```YAML
apiVersion: v1
kind: Pod # Loại tài nguyên là Pod
metadata:
  name: nginx-pod
  labels: # Nhãn (label) rất quan trọng để Service tìm thấy Pod
    app: nginx
spec:
  containers:
  - name: nginx-container
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```
**Lưu ý:** Bạn gần như không bao giờ tạo `Pod` trực tiếp như trên trong production. 
Bạn sẽ dùng `Deployment` để quản lý chúng.   

### 3.2. Khái niệm `Deployment`: Quản lý vòng đời ứng dụng Stateless
`Deployment` là một đối tượng K8s cung cấp các bản cập nhật khai báo (declarative) cho `Pod` và `ReplicaSet`. 
* Bạn khai báo "trạng thái mong muốn" (ví dụ: 3 replicas của image NGINX) trong deployment, 
và `Deployment Controller` (một phần của `kube-controller-manager`) sẽ thay đổi trạng thái thực tế để khớp với trạng thái mong muốn. 
* Nó phù hợp cho các ứng dụng **stateless** (không lưu trạng thái), nơi các Pod là hoàn toàn giống hệt nhau và có thể bị thay thế bất cứ lúc nào. 
* **Cập nhật (Rolling Update) và Rollback:**
  * `Rolling Update`: Khi bạn cập nhật (ví dụ: đổi image tag), `Deployment` sẽ tạo một ReplicaSet mới và dần dần thay thế các Pod cũ bằng Pod mới. 
Nó đảm bảo một số lượng Pod mới. Nó đảm bảo một số lượng Pod nhất định luôn sẵn sàng phục vụ traffic, giúp việc cập nhật không bị gián đoạn (zero downtime).
  * `Rollback`: Nếu bạn cập nhật mới (revision) bị lỗi, K8s lưu lại các revision cũ. Bạn có thể ra lệnh `kubectl rollout undo` và `Deployment` sẽ tự động
quay lui revision ổn định trước đó. 

Một chi tiết kỹ thuật quan trọng là mối quan hệ giũa các đối tượng: `Deployment` không trực tiếp tạo ra `Pod`. Thay vào đó, `Deployment` tạo ra và quản lý `ReplicaSet`. 
`ReplicaSet` mới là đối tượng chịu trách nhiệm duy trì đúng số lượng `replicas` của `Pod`. Khi bạn cập nhật `Deployment` (ví dụ: thay đổi image), nó sẽ tạo ra một `ReplicaSet`
mới và điều phối việc scale-up (tăng) `ReplicaSet` mới, đồng thời scale-down (giảm) `ReplicaSet` cũ. Kiến trúc 3 lớp này chính là cơ chế kỹ thuật cho phép `Rolling Update` và `Rollback` hoạt động.  

Ví dụ YAML: Một `Deployment` NGINX
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3 # TRẠNG THÁI MONG MUỐN: Luôn chạy 3 bản sao
  selector: # Deployment này quản lý Pod nào?
    matchLabels:
      app: nginx # Nó quản lý mọi Pod có nhãn "app: nginx"
  template: # Đây là "khuôn mẫu" (template) để tạo Pod
    metadata:
      labels:
        app: nginx # Pod được tạo ra sẽ có nhãn này (để khớp selector)
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2 # Image để chạy
        ports:
        - containerPort: 80
```
### 3.3. Khái niệm `Service`: Kết nối Microservices với nhau 

**Vấn đề:** `Pod` là phù du (ephemeral). Chúng bị tạo ra và huỷ đi liên tục (do crash, update, auto-scale). Mỗi `pod` mới được tạo ra sẽ có một địa chỉ IP mới. 
Vậy làm thế nào để microservices `frontend` có thể gọi `backend` một cách đáng tin cậy? 

**Giải pháp:** `Service` là một đối tượng K8s cung cấp một địa chỉ IP ảo (Virtual IP) ổn định và một "tên DNS" ổn định cho một nhóm các `Pod`.
* Service sử dụng selector (giống như Deployment) để tìm ra nó cần gửi traffic đến những Pod nào (có label khớp).

## Phần 4. Quản lý cấu hình và dữ liệu bền vững
### 4.1. `ConfigMap`: Tiêm cấu hình (Không nhạy cảm)


### 4.2. `Secret`: Quản lý dữ liệu Nhạy cảm


### 4.3. Quản lý lưu trữ bền vững `PersistentVolume` (PV) và `PersistentVolumeClaim` (PVC)

## Phần 5. Quản lý ứng dụng Stateful - Bài toán Database và Message Queue

### 5.1. Tại sao `Deployment` không đủ cho Database

### 5.2. Giới thiệu `StatefulSet`: "Deployment" cho ứng dụng Stateful

### 5.3. `Headless Service`: DNS cho `StatefulSet`

## Phần 6. Đưa ứng dụng ra ngoài - quản lý truy cập với Ingress
### 6.1. Vấn đề của `Service type: LoadBalancer`

### 6.2. Giới thiệu `Ingress`: Bộ định tuyến

### 6.3. Kiến trúc 2 thành phần: `Ingress` và `Ingress Controller`


## Phần 7. Lộ trình thực hành - "Hands on" với Kubernetes
### 7.1. Thiết lập môi trường phát triển (local development)


### 7.2. Làm chủ `kubectl`: Giao tiếp với Cluster


## Phần 8. Đưa vào Production - Hoàn thiện hệ thống Microservices
### 8.1. Quản lý gói ứng dụng với `Helm`

### 8.2. Giám sát (Monitoring): Kiến trúc Prometheous & Grafana

### 8.3. Thu thập Logs: Cuộc chiến của EFK và Loki

### 8.4. Bảo mật cơ bản: `RBAC` (Role-Based Access Control)

## Phần 9. Cấp độ chuyên gia - Quản lý giao tiếp nâng cao với Service Mesh
### 9.1. Khi nào Kubernetes Networking là đủ? 

### 9.2. `Service Mesh` là gì? 


### 9.3. Kiến trúc `Sidecar Proxy`

### 9.4. So sánh Istio và Linkerd

## Phần 10. Tổng kết lộ trình và các bước tiếp theo 

### 10.1. Tóm tắt lộ trình của bạn


### 10.2. Các chủ đề nâng cao tự nghiên cứu