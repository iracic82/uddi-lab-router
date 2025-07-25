###############################################
# ---------- 1️⃣ React build stage ----------- #
###############################################
FROM node:lts-slim AS ui
WORKDIR /ui

# install and cache deps
COPY ui/package*.json ./
RUN npm ci

# bring in the rest of the source and build
COPY ui/ .
RUN npm run build         # outputs files in /ui/dist

###############################################
# ---------- 2️⃣ FastAPI runtime stage ------- #
###############################################
FROM python:3.12-slim

# system packages your build needed last time
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# 👉 bring the pre-built static assets from the ‘ui’ stage
#    into /app/static  (create the folder if it’s missing)
COPY --from=ui /ui/dist/ ./static/

EXPOSE 8000
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
