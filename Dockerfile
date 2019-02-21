FROM python:3.6

ENV DJANGO_ENV=prod

RUN apt update
RUN apt install -y bash bash-completion vim
RUN mkdir -p /opt/morph-service
RUN pip install uwsgi

WORKDIR /opt/morph-service

ADD uwsgi.ini ./
COPY .tox/dist/* dist/
RUN pip install --no-cache-dir --index-url https://bbpteam.epfl.ch/repository/devpi/simple/ $(ls -t $PWD/dist/*.* | head -n 1)

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/morph-service/uwsgi.ini"]
