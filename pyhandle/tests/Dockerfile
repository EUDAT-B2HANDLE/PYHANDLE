# vim:set ft=dockerfile:
FROM       python:2.7.9

RUN        pip install -U "pip < 21.0" && \
           pip install -U "setuptools < 45" && \
           pip install -U "requests==2.23.0"
RUN        pip install \
           mock \
           coverage \
           nose

ADD        . /opt/PYHANDLE
RUN        cd /opt/PYHANDLE && \
           python setup.py install

WORKDIR    /opt/PYHANDLE/pyhandle/tests

CMD ["./docker-entrypoint.sh", "coverage"]