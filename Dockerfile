FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2021-10-26
RUN apk add build-base
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install flask\[async\] aiohttp psycopg2-binary SQLAlchemy
COPY ./app /app
