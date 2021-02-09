FROM python:3.6

ENV DJANGO_ENV=prod

RUN apt update \
    && apt install -y bash bash-completion vim \
    && mkdir -p /opt/morph-service \
    && pip install uwsgi

WORKDIR /opt/morph-service

COPY uwsgi.ini ./
COPY .tox/dist/* dist/
RUN pip install --no-cache-dir --index-url https://bbpteam.epfl.ch/repository/devpi/simple/ $(ls -t $PWD/dist/*.* | head -n 1)

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/morph-service/uwsgi.ini"]
