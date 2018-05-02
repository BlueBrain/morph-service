FROM ubuntu

ENV DJANGO_ENV=prod

RUN apt-get update && apt-get install -y \
    python3 \
    python3-setuptools \
    python3-pip

RUN mkdir -p /opt/morph-service
RUN pip3 install uwsgi
RUN apt install -y cmake
WORKDIR /opt/morph-service

ADD uwsgi.ini ./
COPY dist/* dist/


RUN apt install -y libhdf5-dev


# morphio is not open source yet so we need to checkout the private repo
# as a git submodule and now we install it
COPY morphio/ morphio/
RUN pip3 install ./morphio
# Same for the NeuroM that depends on MorphIO
COPY NeuroM/ NeuroM/
RUN pip3 install ./NeuroM

RUN pip3 install --no-cache-dir $(ls -t $PWD/dist/*.* | head -n 1)

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/morph-service/uwsgi.ini"]
