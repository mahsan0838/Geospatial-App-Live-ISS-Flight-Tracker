# 🛰️ Live ISS & Flight Tracker

A real-time tracking application for the International Space Station (ISS) and global air traffic, deployed on AWS with a complete GitOps CI/CD pipeline.

## 🌍 Live Demo

- **Frontend Map:** `http://98.81.157.252:30310`
- **ISS API:** `http://98.81.157.252:31506/api/iss`
- **Flights API:** `http://98.81.157.252:31506/api/flights`
- **ArgoCD UI:** `https://98.81.157.252:31892` (admin login)

## 📋 Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GitHub    │────▶│ GitHub      │────▶│ Docker      │
│   Repo      │     │ Actions     │     │ Hub         │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │◀────│ AWS EC2     │◀────│ ArgoCD      │
│   (User)    │     │ (k3s)       │     │ Sync        │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │   Redis     │
                    │   Cache     │
                    └─────────────┘
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Containerization | Docker |
| Orchestration | Kubernetes (k3s) |
| Infrastructure | Terraform (AWS) |
| Configuration | Ansible |
| CI/CD | GitHub Actions + ArgoCD |
| Backend | Python FastAPI |
| Frontend | HTML/JavaScript + Leaflet.js |
| Cache | Redis |
| APIs | OpenNotify (ISS) + OpenSky (Flights) |

## 📁 Project Structure

```
.
├── .github/workflows/
│   └── ci.yml
├── argocd/
│   └── application.yaml
├── ansible/
│   └── playbook.yml
├── terraform/
│   └── main.tf
├── k8s/
│   ├── backend.yaml
│   ├── frontend.yaml
│   └── redis.yaml
├── iss-tracker/
│   ├── backend/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend/
│       ├── index.html
│       └── Dockerfile
└── README.md
```

## 🚀 Deployment Instructions

### Prerequisites

- AWS account
- Terraform installed
- kubectl installed
- Docker installed
- GitHub account

### Step 1: Clone Repository

```bash
git clone https://github.com/mahsan0838/Geospatial-App-Live-ISS-Flight-Tracker.git
cd Geospatial-App-Live-ISS-Flight-Tracker
```

### Step 2: Configure AWS Credentials

```bash
aws configure
```

### Step 3: Deploy Infrastructure with Terraform

```bash
cd terraform
terraform init
terraform apply -auto-approve
terraform output public_ip
cd ..
```

### Step 4: Configure Kubernetes

```bash
ssh -i terraform/iss-key.pem ubuntu@<EC2_IP>
sudo cat /etc/rancher/k3s/k3s.yaml
```

### Step 5: Deploy Application

```bash
kubectl apply -f k8s/
kubectl get pods
```

### Step 6: Add Security Group Rules

```bash
aws ec2 authorize-security-group-ingress --group-id <SG_ID> --protocol tcp --port 31506 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id <SG_ID> --protocol tcp --port 30310 --cidr 0.0.0.0/0
```

### Step 7: Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl apply -f argocd/application.yaml
```

## 🔄 CI/CD Pipeline

GitHub Actions builds Docker images and pushes to Docker Hub. ArgoCD syncs changes automatically.

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| /api/iss | GET | Current ISS position |
| /api/flights | GET | Current flights |

## 🗺️ Frontend Features

- Real-time ISS tracking
- Flight tracking
- Interactive map
- Airplane icons

## 🐳 Docker Images

| Service | Image | Port |
|--------|-------|------|
| Backend | 22i0838/iss-backend | 31506 |
| Frontend | 22i0838/iss-frontend | 30310 |
| Redis | redis:alpine | 6379 |

## 🔧 Troubleshooting

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

## 📝 Environment Variables

| Variable | Purpose |
|----------|--------|
| OPENSKY_USERNAME | API username |
| OPENSKY_PASSWORD | API password |

## 🎯 Future Improvements

- Historical tracking
- Authentication
- WebSockets
- Satellite imagery

## 📄 License

Educational use.

## 👨‍💻 Author

Mahsan0838


---

### Step 3.5: Configure EC2 with Ansible

```bash
cd ansible
docker run --rm -it -v ${PWD}:/ansible -v ${PWD}/../terraform/iss-key.pem:/tmp/iss-key.pem -w /ansible python:3.9-slim sh -c "pip install ansible && ansible-playbook -i '<EC2_IP>,' playbook.yml --private-key /tmp/iss-key.pem -u ubuntu"
cd ..
```

---

### Step 8: Verify GitOps Sync

```bash
# Check ArgoCD application status
kubectl get application -n argocd

# Get ArgoCD admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Access ArgoCD UI at https://<EC2_IP>:31892
# Login with username: admin
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (CI)
- Trigger: Push to `master` branch
- Steps:
  1. Build Docker images for backend/frontend
  2. Push to Docker Hub with commit hash tag
  3. Update image tags in `k8s/*.yaml` manifests
  4. Commit and push manifest changes back to repo

### ArgoCD (CD)
- Sync: Automatically every 3 minutes
- Action: Detects manifest changes and applies to k3s cluster
- Policy: Automated sync with prune and self-heal enabled

---

## ✅ Assignment Requirements Met

- [x] Dockerfiles for each microservice
- [x] Terraform (VPC, EC2, Security Groups)
- [x] Ansible playbook for k3s installation
- [x] Kubernetes manifests (Deployments & Services)
- [x] GitHub Actions CI workflow
- [x] ArgoCD CD synchronization
- [x] Complete README documentation
