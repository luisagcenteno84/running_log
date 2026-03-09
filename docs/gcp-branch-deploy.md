# GCP Branch Deployment Blueprint

Use one GitHub repository with two Cloud Build triggers in two separate GCP projects.

## Environment Mapping

- Branch `dev` deploys to project `running-tracker-dev`
- Branch `main` deploys to project `running-tracker-prod`

Both projects can use the same `cloudbuild.yaml` file because the target project is determined by the Cloud Build trigger's GCP project context.

## Shared Build Config

The repository-level pipeline is defined in `cloudbuild.yaml`.

It will:

1. Run `pytest -q`
2. Build the API container from `Dockerfile`
3. Build the Streamlit container from `Dockerfile.web`
4. Push both images to Artifact Registry
5. Deploy the API to Cloud Run
6. Read the API service URL
7. Deploy the Streamlit frontend with the API URL injected

## Dev Trigger

Create this trigger in project `running-tracker-dev`.

- Event: push to branch
- Source repo: this GitHub repository
- Branch regex: `^dev$`
- Config file: `/cloudbuild.yaml`

Expected target resources in `running-tracker-dev`:

- Artifact Registry repo: `running-tracker`
- Cloud Run service: `running-tracker-api`
- Cloud Run service: `running-tracker-web`
- Secret Manager secret: `app-secret-key`
- Service account: `rt-runtime@running-tracker-dev.iam.gserviceaccount.com`

## Prod Trigger

Create this trigger in project `running-tracker-prod`.

- Event: push to branch
- Source repo: this GitHub repository
- Branch regex: `^main$`
- Config file: `/cloudbuild.yaml`

Expected target resources in `running-tracker-prod`:

- Artifact Registry repo: `running-tracker`
- Cloud Run service: `running-tracker-api`
- Cloud Run service: `running-tracker-web`
- Secret Manager secret: `app-secret-key`
- Service account: `rt-runtime@running-tracker-prod.iam.gserviceaccount.com`

## Why This Works

Cloud Build runs inside the GCP project where the trigger is created.

That means:

- the `dev` trigger builds and deploys into `running-tracker-dev`
- the `main` trigger builds and deploys into `running-tracker-prod`

You do not need two different `cloudbuild.yaml` files unless you want different service names, regions, or deployment rules between environments.

## Recommended Guardrails

- Protect `main` in GitHub so only reviewed changes land there
- Let `dev` auto-deploy more freely for testing
- Keep Firestore, secrets, and Cloud Run services isolated per project
- Apply the Artifact Registry cleanup policy in both projects to avoid image storage creep

## Suggested Setup Order

1. Finish setting up `running-tracker-dev`
2. Create the `^dev$` trigger in the dev project
3. Push to `dev` and verify test/build/deploy
4. Mirror the same resource setup in `running-tracker-prod`
5. Create the `^main$` trigger in the prod project
6. Protect `main` and use it for production releases only
