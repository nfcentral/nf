# syntax=docker/dockerfile:experimental

FROM debian:9.7-slim as base_build
RUN rm /etc/apt/apt.conf.d/docker-clean
RUN echo "Binary::apt::APT::Keep-Downloaded-Packages \"1\";" > /etc/apt/apt.conf.d/keep-archives
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get update
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get upgrade -y


FROM scratch as base
COPY --from=base_build / /
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install dumb-init ca-certificates libssl1.1 libreadline7 libffi6 zlib1g libbz2-1.0 libsqlite3-0


FROM base as python_build
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install curl git build-essential libssl-dev libreadline-dev libffi-dev zlib1g-dev libbz2-dev libsqlite3-dev
RUN git clone --depth 1 https://github.com/pyenv/pyenv /python
ENV PYENV_ROOT=/python
RUN /python/bin/pyenv install 3.7.2
ENV PATH="/python/versions/3.7.2/bin:${PATH}"
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements.sys --upgrade pip setuptools wheel
ENV PATH="/requirements.sys/bin:${PATH}"
ENV PYTHONPATH="/requirements.sys/lib/python3.7/site-packages:${PYTHONPATH}"
RUN find /python/versions/3.7.2 -depth \( \( -type d -a \( -name test -o -name tests -o -name __pycache__ \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \) -exec rm -rf '{}' + ;
RUN cp -R /python/versions/3.7.2 /python/versions/3.7.2.clean
RUN rm -rf /python/versions/3.7.2.clean/lib/pkgconfig
RUN rm -rf /python/versions/3.7.2.clean/share/man
RUN rm -rf /python/versions/3.7.2.clean/lib/python3.7/site-packages/*
RUN rm -rf /python/versions/3.7.2.clean/lib/python3.7/ensurepip
RUN rm -rf /python/versions/3.7.2.clean/lib/python3.7/config-*
RUN rm -rf /python/versions/3.7.2.clean/include
RUN rm /python/versions/3.7.2.clean/lib/libpython3.7m.a


FROM base as python
COPY --from=python_build /python/versions/3.7.2.clean /python/versions/3.7.2
ENV PATH="/python/versions/3.7.2/bin:${PATH}"


FROM python_build as requirements
COPY requirements.txt /
ENV PATH="/requirements/bin:${PATH}"
ENV PYTHONPATH="/requirements/lib/python3.7/site-packages:${PYTHONPATH}"
RUN mkdir /requirements
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements -r requirements.txt
RUN find /requirements -type d -name __pycache__ -exec rm -rf '{}' + ;


FROM python as nf
RUN mkdir /nf
RUN mkdir /project
WORKDIR /project
ENV PYTHONPATH="/nf"
COPY --from=requirements /requirements/ /python/versions/3.7.2/
COPY VERSION /nf/
COPY nf.py /nf/
COPY templates/ /nf/templates
COPY nf /nf/
COPY nfcli /nf/
ENTRYPOINT ["/usr/bin/dumb-init", "python", "/nf/nf.py"]
