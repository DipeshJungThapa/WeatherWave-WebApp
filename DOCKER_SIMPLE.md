# 🐳 Simple Docker Setup

## Quick Start

### Option 1: Production Mode (Recommended)
```bash
# Build and run the complete app
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Option 2: Development Mode
```bash
# Run with development profile
docker-compose --profile dev up --build weatherwave-dev

# Access the app
# Frontend: http://localhost:5173
# Backend API: http://localhost:8001
```

## What's Inside

- **Single Dockerfile**: Builds both frontend and backend in one container
- **Multi-stage build**: Frontend is built first, then served via nginx
- **Simple setup**: Only 2 files needed (`Dockerfile` + `docker-compose.yml`)

## For Your Team

1. **Install Docker** (that's it!)
2. **Clone the repo**
3. **Run one command:**
   ```bash
   docker-compose up --build
   ```

## Architecture

```
┌─────────────────────────────────────┐
│              Container              │
├─────────────────────────────────────┤
│ Nginx (Port 80) → Frontend (React)  │
│ Django (Port 8000) → Backend API    │
└─────────────────────────────────────┘
```

## Troubleshooting

- **Port conflicts?** Change ports in `docker-compose.yml`
- **Build issues?** Run `docker system prune` to clean cache
- **View logs?** Run `docker-compose logs -f`

## Environment Variables

- Backend development mode: `DEBUG=1`
- Frontend API URL: Automatically configured to `http://localhost:8000`

That's it! No complex multi-file Docker setup needed. 🎉
