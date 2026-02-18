# cloud-task-api

A cloud‑native Task Management REST API built with Django and Django REST Framework, designed to demonstrate real‑world backend engineering practices including authentication, containerization, infrastructure as code, and Kubernetes deployment on AWS.

This project is intentionally API‑only (no frontend, no templates) and is structured as a portfolio‑ready backend service suitable for production environments.

⸻

🎯 Project Goals
	•	Build a production‑style REST API using Django
	•	Apply clean architecture and REST best practices
	•	Deploy a containerized service to AWS using Terraform and Kubernetes
	•	Demonstrate skills expected of a Cloud / Backend Application Developer

⸻

🧩 What This Application Does

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

🛠 Tech Stack

Backend
	•	Python 3.11
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

📁 Project Structure

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
├── .gitignore
└── README.md


⸻

🚀 Getting Started (Local Development)

1. Clone the Repository

git clone https://github.com/your-username/cloud-task-api.git
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

🔐 Authentication (Planned)
	•	JWT‑based authentication
	•	Token refresh support
	•	User‑scoped task access

⸻

☁️ Deployment Roadmap
	•	Dockerize the Django application
	•	Push images to Amazon ECR
	•	Provision AWS infrastructure with Terraform
	•	Deploy to Kubernetes (EKS)
	•	Configure CI/CD with GitHub Actions

⸻

📌 Why This Project

This project was built to:
	•	Practice cloud‑native backend development
	•	Demonstrate real‑world engineering decisions
	•	Serve as a strong portfolio piece for backend / cloud roles

⸻

📄 License

MIT License