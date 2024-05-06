FROM python:3.12-slim-bullseye

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*