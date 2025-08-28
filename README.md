# Arch Cloud

A full-stack app that scrapes cloud-architecture pages or GitHub Code Search results, runs a lightweight AI parser to extract services/flows/features, stores them in MongoDB, and shows them in a React UI.

- **Backend:** FastAPI, Pydantic, Requests, BeautifulSoup, MongoDB (PyMongo)  
- **AI:** Google Gemini (via `google-generativeai`)  
- **Frontend:** React  
- **Dockerized:** backend, frontend, and MongoDB (for local/dev)

---

## Requirements

- Python ≥ 3.12  
- Node.js ≥ 16, npm ≥ 6, React ≥ 18  
- Docker & Docker Compose

---

## Instructions

Create a `.env` file in the project root (a `default.env` is provided for reference).

Build and run with Docker Compose:

```docker compose up --build```

## Access the Backend app at:

http://localhost:8000/docs#/

## Access the FronEnd app at:

http://localhost:3000/

## Example URLs To Scrape

HTML pages

AWS Architecture Blog — Serverless stream-based processing for real-time insights
https://aws.amazon.com/blogs/architecture/serverless-stream-based-processing-for-real-time-insights/

GitHub Code Search API (the URL itself goes to api.github.com/search/code?...)

Terraform (AWS S3 + Lambda):
https://api.github.com/search/code?q=aws_s3_bucket+aws_lambda_function+language:HCL+extension:tf&per_page=5