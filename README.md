# FastApi-pet

This project demonstrates a full Kubernetes/GitOps stack for a FastAPI application (`shoppet/shop-api`).

- **Application**: FastAPI-based shop API with endpoints for health, readiness, and Swagger UI.
- **Database**: PostgreSQL managed by the CloudNativePG (CNPG) operator.
- **Cache**: Redis (standalone or cluster) via the Bitnami Helm chart.
- **GitOps**: Flux CD with HelmRelease and Kustomize for four environments (dev, test, stage, prod).
- **CI/CD**: GitHub Actions builds and pushes Docker images to Docker Hub.
- **TLS**: cert-manager with self-signed issuer for HTTPS via Traefik ingress.