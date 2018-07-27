FROM python:2.7

ENV DJANGO_ENV=prod

RUN mkdir -p /opt/morph-service
RUN pip install uwsgi

WORKDIR /opt/morph-service

ADD uwsgi.ini ./
COPY dist/* dist/
RUN pip install --no-cache-dir --process-dependency-links --index-url https://bbpteam.epfl.ch/repository/devpi/simple/ $(ls -t $PWD/dist/*.* | head -n 1)

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/morph-service/uwsgi.ini"]
