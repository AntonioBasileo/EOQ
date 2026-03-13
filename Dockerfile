# Dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir
WORKDIR /eoq

COPY requirements.txt ./

# Utente non-root
RUN addgroup --system eoq && adduser --system --ingroup eoq eoq-user

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Permessi
RUN chown -R eoq-user:eoq . && \
    chmod +x scripts/entrypoint.sh

USER eoq-user

# Avvio server
ENTRYPOINT ["./scripts/entrypoint.sh"]