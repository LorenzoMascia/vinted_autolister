# ============================================================================
# FILE: docker/Dockerfile
# Docker configuration
# ============================================================================

FROM python:3.9-slim

WORKDIR /app

# Installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copia tutto il codice
COPY . .

# Imposta PYTHONPATH per includere la directory src
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]