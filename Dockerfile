FROM python:3.12


ENV PYTHONUNBUFFERED = 1
ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR fastapi_billing/

RUN apt-get update &&  \
    apt-get install -y build-essential libpq-dev &&  \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
