## Deployment (Render) and Environment

- Backend primary URL: update frontend/mobile to use your current Render service URL. Example: https://coatvision-mvp-lyxvision.onrender.com
- Required backend envs on Render:
  - `DATABASE_URL`: Supabase Postgres URI
  - `SUPABASE_URL`: https://<project>.supabase.co
  - `SUPABASE_SERVICE_KEY`: service role key (server-only)
  - `NODE_ENV`: production
  - `SECRET_KEY`: generated locally (see scripts/bootstrap-e2e.ps1)
- Frontend envs: see [frontend/.env.example](frontend/.env.example)
  - `VITE_API_URL`: backend base URL
  - `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`
- Mobile envs:
  - Use `EXPO_PUBLIC_API_URL`, `EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY` (never service key)

### Supabase Schema
- Apply via SQL Editor using [supabase/schema.sql](supabase/schema.sql) or run: `supabase/apply-schema.ps1` (requires `psql`).
- Verify RPCs/tables: run `verify_and_cleanup.ps1` after setting `SUPABASE_URL`/`SUPABASE_SERVICE_KEY`.

### Local Quickstart
- Execute [scripts/bootstrap-e2e.ps1](scripts/bootstrap-e2e.ps1) to build backend (Docker), optionally apply schema, and verify.
# CoatVision_MVP

CoatVision is a coating analysis application with a FastAPI backend, React dashboard, and React Native mobile app.

## Active Stack

| Layer | Service |
|---|---|
| Database / Auth / Storage | **Supabase** |
| Frontend deployment | **Netlify** |
| Backend deployment | **Render** |
| Code & PR flow | **GitHub** |

> **Note:** Vercel is **not** used in this project. Fly.io is **not** used in this project. Mobile app deployment is not an active deliverable at this time.

## 🚀 Deploy to Production

**Ready to deploy?** See the deployment guides:
- **[Quick Deploy Guide](./QUICK_DEPLOY.md)** - Fast deployment to Render
- **[Full Deployment Guide](./DEPLOYMENT.md)** - Complete instructions (English)
- **[Norwegian Guide](./DEPLOYMENT_NO.md)** - Norsk deployment guide
- **[Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist
- **[Architecture Overview](./ARCHITECTURE.md)** - System architecture diagrams

## Quick Start

### Prerequisites

- Python 3.10+ (3.11 recommended)
- Node.js 18+ (Node 20 recommended)
- Docker & Docker Compose (optional, for containerized deployment)
- Git

> Tip: Use pyenv and nvm to manage Python/Node versions across projects.

### Clone Repository

```bash
git clone https://github.com/Coatvision/CoatVision_MVP.git
cd CoatVision_MVP
```

### Automated Setup

We provide automation scripts for setting up all components. See `scripts/README.md` for detailed documentation.

#### Linux/macOS

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Set up backend
./scripts/setup-backend.sh setup

# Set up mobile app
./scripts/setup-mobile.sh setup

# Set up dashboard
./scripts/setup-dashboard.sh setup

# Run all tests
./scripts/run-tests.sh all
```

#### Windows (PowerShell)

Open PowerShell as Administrator on first run and (if needed) allow script execution:

```powershell
# Only if you need to change execution policy (Administrator):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

PowerShell instructions to create and activate the virtual environment and run scripts:

```powershell
# Create venv (from repository root)
python -m venv .venv
# Activate in PowerShell (Windows)
.\.venv\Scripts\Activate.ps1

# Install backend requirements (example)
cd backend
pip install -r requirements.txt

# Return to repository root
cd ..

# Run setup scripts (PowerShell versions provided in scripts/)
.\scripts\setup-backend.ps1 -Command setup
.\scripts\setup-dashboard.ps1 -Command setup
.\scripts\setup-mobile.ps1 -Command setup
```

If you prefer CMD instead of PowerShell, use:

```cmd
.venv\Scripts\activate.bat
```

### Docker Deployment (example)

You can run all services with Docker Compose. Create a `.env` file in the repository root (example provided below) and optionally a `docker-compose.override.yml` to customize service settings for local development.

Example .env:

```env
# .env (example)
DATABASE_URL=sqlite:///./data/dev.db
SECRET_KEY=your-secret-key
API_PORT=8000
FRONTEND_PORT=3000
NODE_ENV=development
EXPO_PUBLIC_API_URL=http://localhost:8000
```

Example `docker-compose.override.yml` for local development:

```yaml
version: '3.8'
services:
  backend:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app/backend
  frontend:
    environment:
      - REACT_APP_API_URL=${EXPO_PUBLIC_API_URL}
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app/frontend
```

Start containers:

```bash
# Build and start
docker compose build
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

If your system uses the older `docker-compose` command instead of `docker compose`, replace the command accordingly.

### Environment variables

Create a `.env` file at the repository root (example shown above). Common environment variables used across services:

- DATABASE_URL - Connection string for your database (e.g. Postgres or SQLite)
- SECRET_KEY - App secret used for signing tokens
- API_PORT - Port for the backend API (default: 8000)
- FRONTEND_PORT - Port for the frontend (default: 3000)
- NODE_ENV - development/production
- EXPO_PUBLIC_API_URL - Backend API URL consumed by mobile app

Be careful not to commit secrets. Add `.env` to `.gitignore` if not already present.

## Project Structure

```
CoatVision_MVP/
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── routers/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          # React dashboard
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── mobile/            # React Native/Expo app
│   ├── src/
│   └── package.json
├── scripts/           # Automation scripts
│   ├── setup-backend.sh/.ps1
│   ├── setup-mobile.sh/.ps1
│   ├── setup-dashboard.sh/.ps1
│   ├── deploy-all.sh/.ps1
│   ├── run-tests.sh/.ps1
│   └── README.md
├── tests/             # Test files
├── docker-compose.yml # Docker configuration
├── AI_PLATFORM_STATUS.md         # AI platform investigation results
├── OPENAI_INTEGRATION_GUIDE.md   # Guide for implementing OpenAI
├── AI_FAQ.md                     # Quick answers to common AI questions
└── README.md
```

## AI Features

### Current State

CoatVision includes AI-ready infrastructure but requires configuration to enable full AI capabilities.

**Available Documentation:**
- **[AI_PLATFORM_STATUS.md](./AI_PLATFORM_STATUS.md)** - Current state of AI integration and platform status
- **[OPENAI_INTEGRATION_GUIDE.md](./OPENAI_INTEGRATION_GUIDE.md)** - Step-by-step guide to integrate OpenAI
- **[AI_FAQ.md](./AI_FAQ.md)** - Quick answers to common AI questions

**Current Capabilities:**
- ✅ **OpenCV Image Processing** - Basic edge detection and coating analysis
- ⚠️ **OpenAI Ready** - Dependency installed, awaiting API key configuration
- ⚠️ **LYXbot Agent** - Placeholder endpoints ready for AI integration

**To Enable AI Features:**
1. Set up OpenAI API key in `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```
2. Follow the [OpenAI Integration Guide](./OPENAI_INTEGRATION_GUIDE.md)
3. Restart backend service

**LYXbot AI Assistant:**
- Endpoint: `POST /api/lyxbot/command`
- Status: `GET /api/lyxbot/status`
- Provides conversational AI for coating analysis assistance

For questions about the "Sparks" AI platform or any missing AI features, see [AI_PLATFORM_STATUS.md](./AI_PLATFORM_STATUS.md).

## Development

### Backend Development

```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port ${API_PORT:-8000}
```

### Frontend Development

Use Node.js 18+ (or Node 20). You can use corepack to ensure package manager consistency (pnpm/yarn) or rely on npm.

```bash
cd frontend
# install dependencies
npm ci
# start dev server
npm run dev
```

### Mobile Development

```bash
cd mobile
npm ci
npm start
```

## Testing

Run tests using the test script:

```bash
./scripts/run-tests.sh all      # All tests
./scripts/run-tests.sh backend  # Backend only
./scripts/run-tests.sh quick    # Quick validation
```

Or run backend tests directly with pytest:

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

## Continuous Integration (GitHub Actions)

This repository includes a basic CI workflow (`.github/workflows/ci.yml`) that:
- Installs Python and Node
- Installs dependencies for backend and frontend
- Runs backend tests with pytest and frontend build/tests

## Deployment to Production

### Backend – Render

Deploy the FastAPI backend as a Web Service on [Render](https://dashboard.render.com):

1. **Push to GitHub**: `git push origin main`
2. **Go to Render Dashboard** → "New +" → "Blueprint"
3. **Select repository**: `connielaudal2-cloud/CoatVision_MVP`
4. **Click "Apply"** – Render auto-deploys from `render.yaml`

**What gets deployed via Render:**
- ✅ Backend API (FastAPI/Python)
- ❌ Mobile App – not an active deliverable

### Frontend – Netlify

The React/Vite dashboard (`frontend/`) is deployed to **Netlify** as a static site.

- Build command: `npm ci && npm run build`
- Publish directory: `frontend/dist`
- SPA redirect rule: `/* → /index.html` (configured in `netlify.toml`)
- Set `VITE_API_URL`, `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` in Netlify environment variables

### Database / Auth / Storage – Supabase

This project uses **Supabase** for database, authentication, and storage.

- Schema: see [`supabase/schema.sql`](supabase/schema.sql)
- Apply via Supabase SQL Editor or `supabase/apply-schema.ps1`
- Required backend secrets: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (set in Render, never committed)
- Frontend uses: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (set in Netlify, never committed)

**Deployment Documentation:**
- [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) - Quick start guide
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Complete deployment guide
- [DEPLOYMENT_NO.md](./DEPLOYMENT_NO.md) - Norwegian guide
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture

### Alternative Deployment Options

- **Docker**: Use the included `Dockerfile` and `docker-compose.yml`
- **Manual**: Follow instructions in `DEPLOYMENT.md`

## Contributing

See `CONTRIBUTING.md` for guidelines on how to contribute, run tests locally, and open pull requests.

## Verification Checklist

After setup, verify:

- [ ] Backend responds at http://localhost:8000
- [ ] Health check passes at http://localhost:8000/health
- [ ] Dashboard loads at http://localhost:3000
- [ ] All tests pass with `./scripts/run-tests.sh all`

## License

See LICENSE file for details.
