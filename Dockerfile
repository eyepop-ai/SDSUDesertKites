FROM python:3.12-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apk add --no-cache \
    build-base \
    bash

RUN addgroup -g 1000 appuser && \
    adduser -D -s /bin/bash -u 1000 -G appuser appuser

USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser requirements.txt .

RUN uv venv && uv pip install -r requirements.txt

COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser run.sh .

RUN mkdir -p temp_streamlit results

# Make run.sh executable
RUN chmod +x run.sh

EXPOSE 8501

ENTRYPOINT ["./run.sh"]
