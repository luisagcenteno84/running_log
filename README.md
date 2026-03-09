# Running Tracker Platform

FastAPI backend plus a Streamlit frontend for logging and analyzing running workouts. The app now uses Firestore as its primary database layer so small deployments can stay within Google Cloud's free usage tiers more easily.

## Tech Stack

- Python 3.11+
- FastAPI + OpenAPI docs
- Streamlit frontend
- Google Cloud Firestore
- Docker + Cloud Run

## Project Structure

```text
app/
  main.py
  config.py
  api/
  services/
  models/
  schemas/
  repositories/
  database/
  analytics/
frontend/
  api_client.py
streamlit_app.py
tests/
Dockerfile
requirements.txt
```

## Core Endpoints

- `POST /api/v1/users`
- `POST /api/v1/users/sign-in`
- `POST /api/v1/users/reset-password`
- `GET /api/v1/users`
- `POST /api/v1/runs`
- `GET /api/v1/runs`
- `GET /api/v1/runs/{id}`
- `GET /api/v1/stats`
- `GET /health`

## Local Development

1. Create or repair the local virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

If `.venv` already exists but points at a missing interpreter, recreate it with:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

2. Configure Firestore access.

For local development, the easiest path is the Firestore emulator:

```powershell
gcloud emulators firestore start
```

In another terminal:

```powershell
$env:FIRESTORE_EMULATOR_HOST='127.0.0.1:8081'
$env:GOOGLE_CLOUD_PROJECT='running-tracker-local'
$env:SECRET_KEY='dev-secret'
$env:ENVIRONMENT='development'
```

If you want to use a real GCP project locally instead, set `GOOGLE_APPLICATION_CREDENTIALS` to a service-account key and `GOOGLE_CLOUD_PROJECT` to your project id.

3. Run the API:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

4. In a second terminal, run the Streamlit frontend:

```powershell
.\.venv\Scripts\activate
$env:RUNNING_TRACKER_API_URL='http://127.0.0.1:8000'
.\.venv\Scripts\python -m streamlit run streamlit_app.py
```

5. Open:

- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:8501`

## Testing

```powershell
.\.venv\Scripts\python -m pytest -q
```

## Lowest-Cost GCP Setup

Use these components for the current architecture:

- `Cloud Run` for the FastAPI API
- `Cloud Run` for the Streamlit frontend
- `Firestore` in Native mode for application data
- `Secret Manager` for secrets
- `Artifact Registry` for container images
- `Cloud Logging` for logs

Optional only when needed:

- `Cloud Storage` for route files or GPX uploads

## Deployment Notes

Set these environment variables on Cloud Run:

```text
GOOGLE_CLOUD_PROJECT
SECRET_KEY
ENVIRONMENT
RUNNING_TRACKER_API_URL
```

Example deployment flow:

```bash
gcloud services enable run.googleapis.com firestore.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/running-tracker/running-tracker-api

gcloud run deploy running-tracker-api \
  --image REGION-docker.pkg.dev/PROJECT_ID/running-tracker/running-tracker-api \
  --platform managed \
  --region REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=PROJECT_ID,ENVIRONMENT=production \
  --set-secrets SECRET_KEY=SECRET_KEY:latest
```

Deploy the Streamlit service similarly, with `RUNNING_TRACKER_API_URL` pointed at the API service URL.

## Notes

- Firestore is schemaless, so there are no SQL migrations in this version.
- The current password-reset flow is suitable for local/dev use, but production should use tokenized email-based reset links.
- For very small workloads, this stack can stay inside free usage tiers, but it is not guaranteed to remain free if usage grows or you enable paid extras.
