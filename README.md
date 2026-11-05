# FastAPI Kubernetes Demo

A small FastAPI service to demonstrate a container-to-Kubernetes GitOps workflow.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/api/v1/hello/{name}` | Greeting endpoint |
| GET | `/docs` | Interactive OpenAPI documentation |

## Run locally

Python 3.12 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Run tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Build and run with Docker

```bash
docker build -t fastapi-k8s-demo:local .
docker run --rm -p 8000:8000 fastapi-k8s-demo:local
```

Open http://localhost:8000/health.

## CI: build and push to GHCR

The GitHub Actions workflow at `.github/workflows/build-and-push.yml` builds the image on every push to `main` and publishes it to:

`ghcr.io/dmanotrl-blip/fastapi-k8s-demo`

It uses the repository-provided `GITHUB_TOKEN`; no personal access token is required for this workflow. Check the Actions tab for the build result. If the package is private, configure Kubernetes image-pull credentials before deploying.

## Deploy to Kubernetes

After the GitHub Actions workflow has successfully published the image:

```bash
kubectl apply -f k8s/
kubectl rollout status deployment/fastapi-demo
kubectl get pods -l app=fastapi-demo
kubectl get svc fastapi-demo
```

The Service uses NodePort `30081`. If the VM firewall and Azure network security group allow inbound TCP 30081, test:

```bash
curl http://<VM-PUBLIC-IP>:30081/health
```

For a private or production cluster, prefer an Ingress or LoadBalancer with TLS rather than exposing a NodePort directly.

## Argo CD

Create an Argo CD application with:

- **Application name:** `fastapi-demo`
- **Project:** `default`
- **Repository URL:** `https://github.com/dmanotrl-blip/fastapi-k8s-demo.git`
- **Revision:** `HEAD`
- **Path:** `k8s`
- **Destination:** `https://kubernetes.default.svc`
- **Namespace:** `default`

Enable automated sync and self-heal if you want Argo CD to reconcile the cluster with Git.

> Note: this demo uses the `latest` image tag for simplicity. For a production GitOps pipeline, use immutable image tags (such as the commit SHA) and update the image tag in the deployment manifest through a separate GitOps update step.
