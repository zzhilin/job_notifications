FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY job_notifications /app/job_notifications
COPY tests /app/tests

RUN pip install --no-cache-dir .[playwright]

CMD ["job-notifications"]
