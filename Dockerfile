FROM python:3.8-slim-buster
ENV PYTHONPATH $PYTHONPATH:/app
ENV PYTHONUNBUFFERED 1

ENV HOST 0.0.0.0
ENV PORT 8000
ENV FLASK_ENV "production"
ENV SQLALCHEMY_DATABASE_URI postgresql+psycopg2://pguser:pgpass@pghost/dbname
ENV CELERY_BROKER_URL sqla+postgresql://pguser:pgpass@pghost/dbname

RUN groupadd --gid 10001 app && \
    useradd --uid 10001 --gid 10001 --shell /usr/sbin/nologin app
RUN install -o app -g app -d /var/run/app /var/log/app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
        apt-get upgrade -y && \
        apt-get install --no-install-recommends -y \
            apt-transport-https \
            ca-certificates \
            build-essential \
            curl \
            libpq-dev

WORKDIR /app

COPY . /app/
RUN pip install --upgrade --no-cache-dir -r requirements/defaults.txt

RUN curl -o /opt/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
      chmod +x /opt/wait-for-it.sh

USER app

ENTRYPOINT [ ]
CMD ["gunicorn", "--chdir", "src", "src.web.wsgi:app"]
