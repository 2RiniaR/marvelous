# Build
FROM python:3.8 as builder
WORKDIR /app
COPY ./Pipfile ./Pipfile.lock /app/
RUN pip install pipenv && \
    pipenv install --system

# Run
FROM python:3.8-slim as runner
WORKDIR /app
ENV PYTHONBUFFERED=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV APP_SETTINGS_FILE_PATH="/app/settings/settings.json"
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY . /app
WORKDIR /app/src
CMD ["python", "./runner.py"]
