# Zero-egress alpine runner
FROM python:3.12-alpine

# Create non-root user
RUN addgroup -S smaos && adduser -S smaos -G smaos
USER smaos

WORKDIR /app
COPY --chown=smaos:smaos . /app

# Ensure no external dependencies are required
ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "smaos_audit.reporter"]
