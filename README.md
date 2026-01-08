# Shape Manager Project

This is my submission for the internship assignment. It uses FastAPI for the backend and React (Vite) for the frontend.

## How to Run

I recommend using Docker:

1. Unzip the file.
2. Run command: `docker-compose up --build`
3. Go to http://localhost:5173

If you want to run it without Docker:

### Backend
1. Go to `backend` folder.
2. Install python packages: `pip install -r requirements.txt`
3. Run: `uvicorn backend.main:app --reload`
4. Make sure you have MySQL and Redis running on localhost.

### Frontend
1. Go to `frontend` folder.
2. Run `npm install`
3. Run `npm run dev`

The app uses:
- FastAPI (Python)
- React
- MySQL
- Redis (for real-time updates)

## Features
- **Admin Portal**: Create and delete shapes.
- **User Portal**: View-only mode for safety.

