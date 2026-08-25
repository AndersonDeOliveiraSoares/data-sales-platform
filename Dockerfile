FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml .
COPY src ./src
COPY scripts ./scripts
COPY migrations ./migrations
COPY alembic.ini .

RUN pip install --no-cache-dir .

COPY . .

CMD ["python", "-m", "src.pipeline"]