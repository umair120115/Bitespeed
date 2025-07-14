# Bitespeed Problem Solution

A fully containerized Django REST Framework (DRF) backend API deployed on Render with a PostgreSQL instance. The project is structured for scalable deployment on platforms like Render, Google Cloud Platform (GCP), AWS, or any Docker-compatible hosting service.
Required API's are live and can be tested wither on Postman or can be integrated to any other platform as it's a REST API.
## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL (hosted on Render)
- **Containerization:** Docker, Docker Compose
- **Deployment:** Render (with GCP and AWS ready configurations)
- **API Documentation:** Swagger / DRF Browsable API


## ✨ Features

- RESTful API endpoints
- Token-based authentication (JWT or DRF Token)
- PostgreSQL database integration
- Swagger/OpenAPI support
- Dockerized for portability
- Environment-specific configuration support
- Ready-to-deploy to Render, GCP, AWS
- api design for the proposed problem

## Running Locally
 ### Step1
- git clone [https://www.github.com/umair120115/Bitespeed](https://github.com/umair120115/Bitespeed.git)
 ### Step2
- create virtual env with command - py -m venv NAME_VENV
- activate virtual env, command - NAME_VENV\Scripts\activate (windows)
- move to the app directory, command - cd core
 ### Step3
- Install dependencies, command - pip install -r requirements.txt
- Configure your environment variables by creating a .env file like DJANGO_SECRET_KEY, DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASSWORD, etc.
- run the app and access on the port 8000, command - py manage.py runserver 8000

## Containerising Application
 ### Step1
- CONFIGURE your DOPPLER_SECRETS and get the DOPPLER_TOKEN
 ### Step2
- In dir core, run - docker compose build
- After image of the container is build, run the container by passing the port (8000) and passing the environment variable in the container as your DOPPLER_TOKEN
- See your application on - http://localhost:8000/


### **API Documentation**
```markdown
## 📘 API Documentation


- Swagger UI: `https://bitespeed-bagl.onrender.com/swagger/`
- List of Contacts in DB: `https://bitespeed-bagl.onrender.com/api/orders/contacts/`
- Bitspeed Problem Solving API ( POST, Fields - email, phoneNumber) : `https://bitespeed-bagl.onrender.com/api/orders/identify/`
```

###  **Note**

```
Thank you very much for providing such an interesting problem.
I have enjoyed while solving this problem and also faced quite challenges.I have tested each case that is mentioned in the problem quotation.
Waiting for the response from your side and it's request please check it before 29 days as it's db has free tier from render,
and will expire after 29 days. i am excited to joing such a fantastic organization and want to make some real committments.
Thanks and regards,
Umair Ahmad
```
