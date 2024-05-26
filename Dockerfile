FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    postgis* \
    supervisor

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["supervisord", "-c", "./supervisord.conf"]
