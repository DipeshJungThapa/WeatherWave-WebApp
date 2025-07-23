# Multi-stage Dockerfile for WeatherWave App
# This single Dockerfile handles both frontend and backend

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with Frontend served
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Backend setup
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Configure nginx
RUN echo 'server { \
    listen 80; \
    location / { \
        root /app/frontend/dist; \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://127.0.0.1:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
    } \
}' > /etc/nginx/sites-available/default

# Create startup script
RUN echo '#!/bin/bash \n\
cd /app/backend \n\
python manage.py migrate \n\
python manage.py runserver 0.0.0.0:8000 & \n\
nginx -g "daemon off;"' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 80 8000

# Start both services
CMD ["/app/start.sh"]
