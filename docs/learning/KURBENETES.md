# Kubernetes: Từ Docker Compose đến quản lý microservices chuyên nghiệp


## Mục lục

[Giới thiệu: Vượt qua giới hạn của Docker](#giới-thiệu-vượt-qua-giới-hạn-của-docker)

[Phần 1: Bước nhảy vọt về tư duy - từ Docker Compose đến điều phối](#phần-1-bước-nhảy-vọt-về-tư-duy---từ-docker-compose-đến-điều-phối)
* [1.1. Từ "vật cưng" (pets) đến "gia súc" (cattle)](#11-từ-vật-cưng-pets-đến-gia-súc-cattle)
* [1.2. Điều phối Container (Container Orchestration) là gì?](#12-điều-phối-container-container-orchestration-là-gì)

[Phần 2: Kiến trúc tổng quan của Kubernetes (K8s 101)](#phần-2-kiến-trúc-tổng-quan-của-kubernetes-k8s-101)
* [2.1. Control Plane: Bộ não của Cụm](#21-control-plane-bộ-não-của-cụm)
* [2.2. Worker Nodes: Cơ bắp của Cụm](#22-worker-nodes-cơ-bắp-của-cụm)

[Phần 3: Các khái niệm cốt lõi trong ứng dụng stateless](#phần-3-các-khái-niệm-cốt-lõi-trong-ứng-dụng-stateless)
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


## Phần 1: Bước nhảy vọt về tư duy - từ Docker Compose đến điều phối
### 1.1. Từ "vật cưng" (pets) đến "gia súc" (cattle)

### 1.2. Điều phối Container (Container Orchestration) là gì?


## Phần 2: Kiến trúc tổng quan của Kubernetes (K8s 101)
### 2.1. Control Plane: Bộ não của Cụm

### 2.2. Worker Nodes: Cơ bắp của Cụm


Dưới dây là bảng tóm tắt kiến trúc K8s:

**Bảng 1: Các thành phần chính của Kubernetes Cluster**


## Phần 3: Các khái niệm cốt lõi trong ứng dụng stateless
### 3.1. Khái niệm `Pod`: Đơn vị triển khai nhỏ nhất

### 3.2. Khái niệm `Deployment`: Quản lý vòng đời ứng dụng tateless

### 3.3. Khái niệm `Service`: Kết nối các Microservices với nhau

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