FROM python:3.11-slim

# Create appuser group and user
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -ms /bin/bash appuser

# Upgrade pip and install virtualenv
RUN pip3 install --no-cache-dir --upgrade \
    pip \
    virtualenv

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Switch to appuser
USER appuser
WORKDIR /home/appuser

# Copy application files
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser .env* ./
COPY --chown=appuser:appuser .streamlit .streamlit

# Create and activate virtual environment, then install dependencies
ENV VIRTUAL_ENV=/home/appuser/venv
RUN virtualenv ${VIRTUAL_ENV}
RUN . ${VIRTUAL_ENV}/bin/activate && pip install --no-cache-dir -r requirements.txt

# Create directories for persistent data
RUN mkdir -p temp_streamlit results

# Copy run script
COPY --chown=appuser:appuser run.sh /home/appuser/
RUN chmod +x /home/appuser/run.sh

# Expose Streamlit port
EXPOSE 8501

# Run the application
ENTRYPOINT ["./run.sh"]
