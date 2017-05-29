# vim:set ft=dockerfile:
FROM       eudat-pyhandle

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
