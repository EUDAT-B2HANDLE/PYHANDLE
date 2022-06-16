# vim:set ft=dockerfile:
FROM       python:2.7.9


#RUN        easy_install pip
#RUN        pip install \
#           mock \
#           coverage \
#           nose

RUN        pip install -U "pip < 21.0" && \
           pip install -U "setuptools < 45" && \
           pip install -U "requests==2.23.0" && \
           pip install -U "pymysql==0.8.0" 
           
RUN        pip install \
           mock \
           coverage \
           nose

#VOLUME     /opt/PYHANDLE/pyhandle/tests
#WORKDIR    /opt/PYHANDLE/pyhandle/tests

#COPY       docker-entrypoint.sh ./

#ENTRYPOINT ["./docker-entrypoint.sh"]

#CMD        ["coverage"]
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD        . /opt/PYHANDLE
RUN        cd /opt/PYHANDLE && \
           python setup.py install

WORKDIR    /opt/PYHANDLE/pyhandle/tests
CMD ["./docker-entrypoint.sh", "coverage"]

#COPY       docker-entrypoint.sh ./
#ENTRYPOINT ["./docker-entrypoint.sh"]
#CMD ["coverage"]


#RUN        cd /opt/PYHANDLE && \
#           python setup.py test

#ENTRYPOINT ["sh", "./docker-entrypoint.sh"]

#CMD        ["coverage"]


# TODO: Document build + usage of this Dockerfile.

