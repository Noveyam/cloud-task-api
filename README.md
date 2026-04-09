# Cloud-Native Task Management API

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-rest--framework-green)
![Docker](https://img.shields.io/badge/docker-containerized-blue)
![AWS](https://img.shields.io/badge/aws-eks%20%7C%20cloudwatch-orange)
![Terraform](https://img.shields.io/badge/terraform-infrastructure-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A cloud-native Task Management REST API built with Django and Django REST Framework. This project demonstrates backend API development, JWT authentication, Docker containerization, Terraform-based infrastructure, Kubernetes deployment on AWS, and production-style monitoring with CloudWatch.

## Highlights

- REST API built with Django REST Framework
- JWT authentication for protected routes
- Per-user task access control
- Dockerized application for consistent deployment
- AWS deployment with Kubernetes and Application Load Balancer
- Terraform-managed infrastructure
- Health checks and CloudWatch alarm coverage for operational monitoring

## Features

Authenticated users can:

- Register and log in
- Create tasks
- List their own tasks
- Retrieve individual tasks
- Update tasks
- Delete tasks

## Architecture

Client  
→ AWS Application Load Balancer  
→ Kubernetes Service / Ingress  
→ Django API containers on Amazon EKS  
→ Amazon RDS (PostgreSQL)

Background processing:

Django API  
→ Redis broker  
→ Celery worker  
→ Database / async task execution

Monitoring and alerting:

Application / Kubernetes / ALB metrics / logs
→ Amazon CloudWatch  
→ Alarm-based alerting

## API Endpoints

### Authentication

```http
POST /auth/register/
POST /auth/login/
POST /auth/refresh/
```

### Tasks

```http
GET    /tasks/
POST   /tasks/
GET    /tasks/{id}/
PUT    /tasks/{id}/
DELETE /tasks/{id}/
```

All task routes require JWT authentication.

## Health Check

```http
GET /health/
```

Example response:

```json
{"status":"ok"}
```

## Tech Stack

**Backend**
- Python
- Django
- Django REST Framework
- JWT Authentication
- Celery

**Data / Messaging**
- PostgreSQL
- Amazon RDS
- Redis

**Infrastructure / DevOps**
- Docker
- Terraform
- Kubernetes
- Amazon EKS
- AWS Application Load Balancer
- Amazon CloudWatch
- Amazon ECR
- IAM

**Development**
- SQLite for early local development
- Git / GitHub
- Linux/macOS CLI tooling

## Security

- JWT authentication on protected routes
- User-level data isolation
- Non-root container execution
- Environment-variable based configuration
- IAM-managed cloud access patterns
- Health endpoint for service validation and monitoring

## Background Processing

The project uses Redis and Celery to support asynchronous task execution and to extend the API beyond simple request/response handling. This makes the architecture more production-oriented and provides a foundation for scheduled jobs, retries, and longer-running background workflows.

## Monitoring

CloudWatch alarm coverage includes:

- ALB healthy targets low
- ALB unhealthy targets
- ALB target 5xx responses
- Application error patterns
- Pod pending state
- Container waiting state
- CPU utilization
- Memory utilization
- Latency
- Cluster pod capacity usage

## Local Development

Clone the repository:

```bash
git clone https://github.com/Noveyam/cloud-task-api.git
cd cloud-task-api
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python3 manage.py migrate
```

Start the development server:

```bash
python3 manage.py runserver
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health/
```

## Run with Docker

Build the image:

```bash
docker build -t cloud-task-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 \
  -e DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost" \
  -e DJANGO_SECRET_KEY="your-secret-key" \
  cloud-task-api
```

## Project Status

**Completed**
- Task CRUD API
- JWT authentication
- Docker containerization
- Terraform-managed AWS infrastructure
- Amazon EKS deployment
- Amazon RDS integration
- Redis and Celery integration
- CloudWatch alarm setup and validation
- Health check and monitoring improvements

**In Progress**
- Terraform cleanup and infrastructure alignment
- EKS access entry management
- Pod identity association cleanup
- CloudWatch add-on standardization
- CI/CD improvements
- Documentation refresh

## Why This Project

This project was built to demonstrate practical backend and cloud engineering skills, including API design, authentication, containerization, infrastructure as code, cloud deployment, monitoring, and troubleshooting.

## Production-Focused Work

This project includes production-oriented engineering work such as:

- Infrastructure as code with Terraform
- Kubernetes deployment on Amazon EKS
- Managed PostgreSQL with Amazon RDS
- Redis and Celery for asynchronous processing
- ALB health checks and traffic routing
- CloudWatch alarms for API, ALB, pod, container, CPU, memory, latency, and capacity signals
- Ongoing infrastructure cleanup to reduce manual operational steps