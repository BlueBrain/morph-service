FROM python:3.6

ENV DJANGO_ENV=prod

RUN mkdir /code
RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi


WORKDIR /code

ADD requirements.txt /code/

RUN pip3 install -r requirements.txt

ADD . /code/

EXPOSE 8000

CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]
