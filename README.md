# Cloud Task Management API
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-rest--api-green)
![Docker](https://img.shields.io/badge/docker-containerized-blue)
![AWS](https://img.shields.io/badge/aws-ec2-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A cloud‑native Task Management REST API built with Django and Django REST Framework, designed to demonstrate real‑world backend engineering practices including authentication, containerization, infrastructure as code, and Kubernetes deployment on AWS.

This project is intentionally API‑only (no frontend, no templates) and is structured as a portfolio‑ready backend service suitable for production environments.

⸻

Project Goals
	•	Build a production‑style REST API using Django
	•	Apply clean architecture and REST best practices
	•	Deploy a containerized service to AWS using Terraform and Kubernetes
	•	Demonstrate skills expected of a Cloud / Backend Application Developer

⸻

What This Application Does

The API allows authenticated users to:
	•	Register and authenticate using JWT
	•	Create, update, delete, and list tasks
	•	Mark tasks as complete or incomplete
	•	Retrieve only their own tasks

The service is designed to be:
	•	Stateless
	•	Secure
	•	Easily deployable to cloud infrastructure

⸻

Architecture Diagram (Request Flow)

                       (Public Internet)
                              |
                              |  HTTP :80
                              v
+-------------------+   +------------------------+
| Client            |-->| EC2 Security Group     |
| (Browser / curl)  |   | Inbound: 80 (and 22*)  |
+-------------------+   +------------------------+
                              |
                              v
                    +----------------------+
                    | Nginx (Reverse Proxy)|
                    | Listens on :80       |
                    +----------+-----------+
                               |
                               | proxy_pass to localhost:8000
                               v
                    +----------------------+
                    | Uvicorn (ASGI)       |
                    | Listens on 127.0.0.1 |
                    | :8000 (private)      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Django + DRF         |
                    | /health/, /tasks/    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Database             |
                    | SQLite (dev)         |
                    | Postgres (prod)      |
                    +----------------------+

*SSH :22 should be restricted to your IP (x.x.x.x/32)

Client → Nginx (80) → Uvicorn (127.0.0.1:8000) → Django → Database

The application is deployed on an EC2 instance running Amazon Linux. Nginx acts as a reverse proxy on port 80, forwarding traffic to Uvicorn running on localhost:8000. Django REST Framework handles API requests, authentication via JWT, and database operations. Uvicorn is managed by systemd for automatic restarts and background execution. This architecture separates public HTTP handling from application execution, following production deployment best practices.

⸻

Live Deployment

Public Health Check:

http://18.209.7.86/health/

Example Response:

{"status": "ok"}

⸻

API Endpoints

#Authentication

POST /auth/register/
POST /auth/login/
POST /auth/refresh/

#Tasks

GET    /tasks/
POST   /tasks/
GET    /tasks/{id}/
PUT    /tasks/{id}/
DELETE /tasks/{id}/

All task routes require JWT authentication.

⸻

Security Design

- Port 8000 is not publicly exposed
- Only Nginx (port 80) is accessible externally
- Django ALLOWED_HOSTS enforced
- JWT authentication protects task routes
- User-level access control prevents cross-user data access
- Uvicorn runs as a non-root user

⸻

Containerization

The application is containerized using Docker.

Key container features:

- Multi-stage Docker build
- Non-root container user
- Optimized image size
- Uvicorn ASGI server for production workloads

⸻

Health Check

The API exposes a health endpoint used for monitoring and container orchestration.

Endpoint:

GET /health/

Example response:

{
  "status": "ok"
}

This endpoint can be used by:

- Docker health checks
- Kubernetes liveness probes
- Load balancer monitoring

⸻

🛠 Tech Stack

Backend
	•	Python 3.12
	•	Django
	•	Django REST Framework
	•	JWT Authentication

Infrastructure & DevOps
	•	Docker
	•	Kubernetes (EKS)
	•	Terraform
	•	AWS (ECR, EKS, RDS, IAM)
	•	GitHub Actions (CI/CD)

Development
	•	SQLite (local development)
	•	PostgreSQL (production)
	•	Linux‑based tooling

⸻

Project Structure

cloud-task-api/
├── config/            # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── tasks/             # Core application logic
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md

⸻

Getting Started (Local Development)

1. Clone the Repository

git clone https://github.com/Noveyam/cloud-task-api.git
cd cloud-task-api

2. Create Virtual Environment

python -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Run Migrations

python manage.py migrate

5. Start Development Server

python manage.py runserver

6. Health Check

GET http://127.0.0.1:8000/health/

Expected response:

{"status": "ok"}

⸻

Run Locally with Docker

The API can also be run using Docker.

Build the image:

docker build -t cloud-task-api .

Run the container:

docker run --rm -p 8000:8000 \
  -e DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost" \
  cloud-task-api

Test the health endpoint:

curl http://127.0.0.1:8000/health/

Environment Variables

The application uses environment variables for configuration.

Example:

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECRET_KEY=your-secret-key

A sample configuration file is provided:

.env.example

⸻

Deployment Status

#Current
- EC2 deployment with Nginx + Uvicorn
- Systemd-managed app service
- SQLite database
- Public health check endpoint
- Docker containerization

#Planned
- Terraform infrastructure provisioning
- Deployment to Kubernetes (EKS)
- PostgreSQL via Amazon RDS
- CI/CD via GitHub Actions

⸻

Why This Project

This project was built to:
	•	Practice cloud‑native backend development
	•	Demonstrate real‑world engineering decisions
	•	Serve as a strong portfolio piece for backend / cloud roles

⸻

