# vim:set ft=dockerfile:
FROM       python:2.7.9

RUN        pip install -U "pip < 21.0" && \
           pip install -U "setuptools < 45" && \
           pip install -U "requests==2.23.0" && \
           pip install -U "pymysql==0.8.0" && \
           pip install -U "mock==3.0.5" 
           
RUN        pip install \
           coverage \
           nose

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD        . /opt/PYHANDLE
RUN        cd /opt/PYHANDLE && \
           python setup.py install

WORKDIR    /opt/PYHANDLE/pyhandle/tests

CMD ["./docker-entrypoint.sh", "coverage"]
