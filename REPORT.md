# ACEest Fitness & Gym — DevOps CI/CD Report

## 1. CI/CD Architecture Overview
The pipeline follows this flow:
GitHub → Jenkins → Pytest → Docker Build → 
Docker Hub → Kubernetes (Minikube)

Tools used:
- Version Control: Git & GitHub
- CI Server: Jenkins (Docker container)
- Testing: Pytest (8 test cases)
- Containerization: Docker
- Registry: Docker Hub (meghabarua/aceest-fitness)
- Orchestration: Minikube/Kubernetes

## 2. Deployment Strategies Implemented
1. Rolling Update - Zero downtime incremental updates
2. Blue-Green - Instant traffic switching between versions
3. Canary - 20% traffic to new version for testing
4. Shadow - Mirror traffic to test new version silently
5. A/B Testing - Split traffic between variant A and B

## 3. Challenges Faced & Mitigations
- Jenkins Docker socket not mounted → Recreated container with socket
- kubectl not found in Jenkins → Installed manually inside container
- Kube config permission denied → Copied config to jenkins_home
- Image name placeholders → Used sed to replace in all YAML files

## 4. Key Automation Outcomes
- Every git push triggers automatic build
- 8 unit tests run automatically on every build
- Docker image auto-built and pushed to Docker Hub
- Zero-downtime deployments via Kubernetes
- Rollback capability via kubectl rollout undo
