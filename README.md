# Hospital Token System: DevOps Project

A simple hospital OP token system, built as a hands-on DevOps project. Each doctor has a separate token queue, like a real OP counter.

The focus of this project is the DevOps part: containerizing the app and deploying it on AWS with Infrastructure as Code and a CI/CD pipeline.

## Tech Stack

- Python (Flask)
- Docker
- PostgreSQL
- Docker Compose
- Terraform
- AWS (EC2, Security Groups)
- Git and GitHub

## API Endpoints

| Endpoint | What it does |
|---|---|
| `/` | Home page |
| `/token/<doctor>/new` | Generate a new token for a doctor |
| `/token/<doctor>/list` | List all tokens of a doctor |
| `/health` | Health check |

Doctors available: `dr-anil`, `dr-meera`, `dr-suresh`

## Run with Docker

```
docker compose up --build
```

Then open `http://localhost:5000/token/dr-anil/new` in the browser.

## Project Progress

- [x] Flask app
- [x] Dockerfile
- [x] PostgreSQL database with docker-compose
- [x] AWS infrastructure with Terraform
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Monitoring with Prometheus and Grafana