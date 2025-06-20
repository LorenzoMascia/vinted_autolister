# ============================================================================
# FILE: docker/Dockerfile
# Docker configuration
# ============================================================================

FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]