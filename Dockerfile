FROM python:3.6

ENV DJANGO_ENV=prod

RUN mkdir -p /opt/morph-service
RUN pip3 install uwsgi

WORKDIR /opt/morph-service

ADD uwsgi.ini ./
COPY dist/* dist/
RUN pip3 install --no-cache-dir $(ls -t $PWD/dist/*.* | head -n 1)

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/morph-service/uwsgi.ini"]
