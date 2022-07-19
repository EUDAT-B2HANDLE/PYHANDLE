# vim:set ft=dockerfile:
FROM       python:3.10


RUN        apt-get update && apt-get install -y --no-install-recommends \
           make \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN        easy_install pip
RUN        pip install \
           sphinx

VOLUME     /opt/PYHANDLE/docs

WORKDIR    /opt/PYHANDLE/docs

ENTRYPOINT ["make"]

CMD        ["help"]
