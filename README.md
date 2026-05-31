# RAG Chatbot CI/CD Pipeline with Kubernetes (Minikube)
Production-style RAG (Retrieval-Augmented Generation) chatbot using modern GenAI and DevOps tools.

This project demonstrates a complete CI/CD pipeline for deploying a Retrieval-Augmented Generation (RAG) chatbot using:

- GitHub Actions
- Docker
- Kubernetes
- Minikube
- Self-hosted GitHub Runner

---

# Project Overview

The application is containerized using Docker and deployed into a Kubernetes cluster managed by Minikube.

The CI/CD pipeline automatically:

1. Pulls the latest source code
2. Starts Minikube
3. Builds the Docker image inside Minikube
4. Creates Kubernetes secrets
5. Deploys the application using Kubernetes manifests
6. Verifies the deployment

---

# Technologies Used

- Python / FastAPI (RAG Application)
- Docker
- Kubernetes
- Minikube
- GitHub Actions
- Self-hosted Runner

---

# CI/CD Workflow Explanation

The GitHub Actions workflow performs the following steps:

## Checkout Code
- uses: actions/checkout@v4
Pulls the latest source code from the repository.

---

## Start Minikube
minikube start --memory=4096 --cpus=2 --driver=docker
Starts a local Kubernetes cluster using Docker as the driver.

---

## Build Docker Image Inside Minikube

eval $(minikube docker-env)
docker build -t rag-app ./RAG_chatbot

Switches Docker environment to Minikube’s internal Docker daemon and builds the image there.

This is necessary because Kubernetes inside Minikube cannot access images built in the host Docker environment.

---

## Create Kubernetes Secret

kubectl create secret generic rag-secret \
--from-literal=GROQ_API_KEY=YOUR_API_KEY

Creates a Kubernetes secret to securely store the API key.

---

## Deploy Application
kubectl apply -f deployment.yml
kubectl apply -f service.yml


Deploys the application to Kubernetes.

### deployment.yml
Defines:
- Pods
- Container image
- Replicas
- Environment variables

### service.yml
Exposes the application using a Kubernetes Service.

---

## Verify Deployment
kubectl get pods
kubectl get svc

Checks whether pods and services are running successfully.

# Required GitHub Secret

Add the following secret in your GitHub repository:

| Secret Name | Description |
|---|---|
| `GROQ_API_KEY` | API key used by the RAG application |

### Add Secret:
GitHub Repository → Settings → Secrets and Variables → Actions → New Repository Secret

---

# Docker Build

Build image manually: docker build -t rag-app ./RAG_chatbot
---

# Kubernetes Deployment

Apply deployment manually:

kubectl apply -f deployment.yml
kubectl apply -f service.yml

Check resources:

kubectl get pods
kubectl get svc

---

# Running the Application

If using Minikube service: minikube service <service-name>

Or port-forward: kubectl port-forward service/<service-name> 8000:8000
---

# Why Minikube is Used

Minikube is used to create a lightweight local Kubernetes cluster for development and testing.

Benefits:
- No cloud cost
- Easy Kubernetes learning
- Local deployment testing
- CI/CD experimentation
- Kubernetes manifest validation

---

# Current Limitation

This project builds the Docker image directly inside Minikube instead of pushing it to a container registry.

For production systems, the recommended approach is:

1. Build image once
2. Push to DockerHub/ECR/ACR
3. Deploy using image registry

---

# Future Improvements

- Use DockerHub or Azure Container Registry
- Implement rolling deployments
- Add ingress controller
- Add monitoring with Prometheus/Grafana
- Deploy to AKS/EKS/GKE
- Add automated testing stage

---

# Key Learning Outcomes

This project demonstrates:
- Docker containerization
- Kubernetes deployment
- GitHub Actions CI/CD
- Kubernetes secrets management
- Self-hosted runner setup
- Minikube-based local orchestration

---
