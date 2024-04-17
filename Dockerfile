FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils\
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
    postgis*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py test && \
    daphne -b 0.0.0.0 -p 8000 vroomvroom.asgi:application & \
    celery -A vroomvroom worker -l info"]
