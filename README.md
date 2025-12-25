git clone https://github.com/Salonikumari95/jobseeker-backend-django.git
djangorestframework-simplejwt (JWT Authentication)

# Jobseeker Backend Django

This is the backend for the Jobseeker platform, built with Django. It provides APIs and web views for job seekers and recruiters, including job posting, applications, community features, chat, and authentication.

## 🚀 Deployed Link

**Live Demo:**https://jobseeker-backend-django.onrender.com
## Features

- User registration and authentication (JWT & session)
- Recruiter and job seeker dashboards
- Job posting, application, and bookmarking
- Community feed with posts, comments, likes, and moderation
- Real-time chat using Django Channels
- Profile management for users
- Password reset via OTP
- Media uploads via Cloudinary

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (or use SQLite for local testing)
- Cloudinary account (for media uploads)

### Installation

1. **Clone the repository:**
	```sh
	git clone https://github.com/Salonikumari95/jobseeker-backend-django.git
	cd jobseeker-backend-django
	```

2. **Create and activate a virtual environment:**
	```sh
	python -m venv env
	env\Scripts\activate   # On Windows
	source env/bin/activate # On Linux/Mac
	```

3. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```

4. **Configure environment variables:**
	- Copy `.env.example` to `.env` and fill in your secrets.

5. **Apply migrations:**
	```sh
	python manage.py migrate
	```

6. **Create a superuser (optional):**
	```sh
	python manage.py createsuperuser
	```

7. **Run the development server:**
	```sh
	python manage.py runserver
	```

## Usage

- Visit the deployed site: [https://django-task-bgej.onrender.com](https://django-task-bgej.onrender.com)
- Register as a job seeker or recruiter.
- Explore dashboards, apply for jobs, post in the community, and chat.

## API Endpoints

- `/auth/` - User authentication and profile APIs
- `/jobs/` - Job posting and application APIs
- `/community/` - Community feed, posts, comments, likes
- `/chat/` - Real-time chat (WebSocket)
- `/dashboard/seeker/` - Job seeker dashboard
- `/dashboard/recruiter/` - Recruiter dashboard

## Technologies Used

- Django & Django REST Framework
- Django Channels (WebSocket chat)
- PostgreSQL
- Cloudinary (media storage)
- JWT Authentication
- Render (deployment)

## License

MIT

## Maintainers

- [Salonikumari95](https://github.com/Salonikumari95)
- [mayank](https://github.com/Manny2706)

---

**For any issues or feature requests, please open an issue on GitHub.**

## Docker (Development)

This repository includes a `Dockerfile` and a `docker-compose.yml` to run the application locally with Postgres and Redis.

Prerequisites: `docker` and `docker-compose` installed.

Build and run:

```bash
docker-compose build
docker-compose up -d
```

for cloud data base 
remove db and redis from docker-compose.yml

The web application will be available at `http://localhost:8000`.

Notes:
- Copy `.env.example` to `.env` and set database credentials before `docker-compose up`.
- The `entrypoint.sh` runs migrations and `collectstatic` on container start. For production you may prefer a different strategy.

To stop and remove containers:

```bash
docker-compose down -v
```

