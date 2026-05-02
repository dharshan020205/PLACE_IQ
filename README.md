# PlaceIQ

PlaceIQ is an AI-Based Placement Readiness Prediction System designed to predict whether a student is placement-ready based on academic and skill-based parameters. It combines a trained Logistic Regression model with a deterministic rule engine.

## Local Development

### 1. Backend Server
The backend is powered by FastAPI, SQLAlchemy (SQLite), and scikit-learn.

1. Open your terminal and navigate to the project root:
   ```bash
   cd D:\placeiq
   ```
2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
3. Run the Uvicorn server as a module:
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```
4. View the interactive Swagger documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend Application
The frontend is a React application built with Vite and Tailwind CSS.

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd D:\placeiq\frontend
   ```
2. Start the Vite dev server:
   ```bash
   npm run dev
   ```
3. View the web app at: [http://localhost:5173](http://localhost:5173)

---

## ⚠️ Important Deployment Warning

**Admin Credentials:** The system is seeded with a default admin user (`admin` / `admin123`). **You MUST change these credentials before deploying to a public environment (like Render).**

**Environment Variables:** When deploying, ensure you configure the following environment variables on your hosting provider:
- `SECRET_KEY` (Backend)
- `DATABASE_URL` (Backend - e.g., your PostgreSQL connection string)
- `ALLOWED_ORIGINS` (Backend - e.g., `https://your-frontend.onrender.com`)
- `VITE_API_URL` (Frontend - e.g., `https://your-backend.onrender.com`)
