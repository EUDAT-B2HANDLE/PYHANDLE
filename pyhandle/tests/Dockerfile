# vim:set ft=dockerfile:
FROM       python:2.7.9


RUN        easy_install pip
RUN        pip install \
           mock \
           coverage \
           nose

VOLUME     /opt/PYHANDLE/pyhandle/tests

WORKDIR    /opt/PYHANDLE/pyhandle/tests

COPY       docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD        ["coverage"]


# TODO: Document build + usage of this Dockerfile.

