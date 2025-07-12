# Patient Copilot

Patient Copilot is an open-source health application that helps patients with chronic or serious illnesses manage their treatment plans, reminders and medical documents. This repository contains a basic scaffold for both the frontend and backend services.

## Tech Stack

- **Flutter** for the cross-platform frontend (Web and iOS)
- **FastAPI** for the backend API
- **SQLite** for lightweight local persistence

## Project Structure

```
backend/   # FastAPI application
frontend/  # Flutter application
docs/      # Project documentation
```

### Frontend
The `frontend` directory contains a minimal Flutter project with placeholders for a login screen and a reminder dashboard.

### Backend
The `backend` directory holds a FastAPI project scaffold with SQLite support, sample API routes, data models and a service layer.


## Development with Docker Compose

1. Copy `.env.example` to `.env` at the repository root and adjust the value as
   needed. This file provides `API_URL` to the frontend service.
2. Create a `.env` file inside the `backend` directory to define variables such
   as `DATABASE_URL` for the FastAPI application.
3. Run `docker-compose up` to start both the backend and Flutter web server.
4. The backend container mounts `./data` on the host to `/app/data` so the
   SQLite database persists between runs.


   The API will be available at `https://api.jeffandsons.us` and the web app at
   `http://localhost:5174`

   When running the Flutter app outside of Docker, pass the API URL using
   `--dart-define`:

   ```bash
   flutter run -d chrome --web-port=5174 --dart-define=API_URL=https://api.jeffandsons.us
   ```

   
### Running the Backend
Create a `.env` file inside the `backend` directory to store environment variables.  
Set `DATABASE_URL` to your database connection string. When this variable is not defined, the backend uses `sqlite:////app/data/patient_copilot.db` by default. The application loads this file automatically at startup. After installing the requirements, run the server from within the `backend` folder:



```bash
pip install -r requirements.txt
./run.sh
```


## Next Steps

- Implement user authentication and authorization
- Flesh out reminder scheduling and notification logic
- Add medical document management features
- Expand tests and documentation
