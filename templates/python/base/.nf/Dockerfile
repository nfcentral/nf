# syntax=docker/dockerfile:experimental


FROM debian:9.7-slim as base_build
RUN rm /etc/apt/apt.conf.d/docker-clean
RUN echo "Binary::apt::APT::Keep-Downloaded-Packages \"1\";" > /etc/apt/apt.conf.d/keep-archives
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get update
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get upgrade -y


FROM scratch as base
COPY --from=base_build / /
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install dumb-init ca-certificates libssl1.1 libreadline7 libffi6 zlib1g libbz2-1.0 libsqlite3-0
ENTRYPOINT ["/usr/bin/dumb-init"]


FROM base as python_build
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install curl git build-essential libssl-dev libreadline-dev libffi-dev zlib1g-dev libbz2-dev libsqlite3-dev
RUN git clone --depth 1 https://github.com/pyenv/pyenv /python
ENV PYENV_ROOT=/python
RUN /python/bin/pyenv install {{python.version}}
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"
ADD nf.pipfreeze /
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements.sys -c /nf.pipfreeze --upgrade pip setuptools wheel
ENV PATH="/requirements.sys/bin:${PATH}"
ENV PYTHONPATH="/requirements.sys/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN find /python/versions/{{python.version}} -depth \( \( -type d -a \( -name test -o -name tests -o -name __pycache__ \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \) -exec rm -rf '{}' + ;
RUN cp -R /python/versions/{{python.version}} /python/versions/{{python.version}}.clean
RUN rm -rf /python/versions/{{python.version}}.clean/lib/pkgconfig
RUN rm -rf /python/versions/{{python.version}}.clean/share/man
RUN rm -rf /python/versions/{{python.version}}.clean/lib/python{{python.version_short}}/site-packages/*
RUN rm -rf /python/versions/{{python.version}}.clean/lib/python{{python.version_short}}/ensurepip
RUN rm -rf /python/versions/{{python.version}}.clean/lib/python{{python.version_short}}/config-*
RUN rm -rf /python/versions/{{python.version}}.clean/include
RUN rm /python/versions/{{python.version}}.clean/lib/libpython{{python.version_short}}m.a


FROM base as python
COPY --from=python_build /python/versions/{{python.version}}.clean /python/versions/{{python.version}}
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"


FROM python_build as requirements
{{#dependencies_nf_build?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_nf_build}} {{_}}{{/dependencies_nf_build}}
{{/dependencies_nf_build?}}
COPY .nf/requirements.nf.txt /
ENV PATH="/requirements.nf/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements.nf -c /nf.pipfreeze -r requirements.nf.txt
RUN find /requirements.nf -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_build?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_build}} {{_}}{{/dependencies_build}}
{{/dependencies_build?}}
COPY requirements.txt /
ENV PATH="/requirements/bin:${PATH}"
ENV PYTHONPATH="/requirements/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements -c /nf.pipfreeze -r requirements.txt
RUN find /requirements -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_nf_dev_build?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_nf_dev_build}} {{_}}{{/dependencies_nf_dev_build}}
{{/dependencies_nf_dev_build?}}
COPY .nf/requirements.nf.dev.txt /
ENV PATH="/requirements.nf.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf.dev
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements.nf.dev -c /nf.pipfreeze -r requirements.nf.dev.txt
RUN find /requirements.nf.dev -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_dev_build?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_dev_build}} {{_}}{{/dependencies_dev_build}}
{{/dependencies_dev_build?}}
COPY requirements.dev.txt /
ENV PATH="/requirements.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.dev
RUN --mount=id=nfpip,target=/root/.cache/pip,type=cache pip install --prefix /requirements.dev -c /nf.pipfreeze -r requirements.dev.txt
RUN find /requirements.dev -type d -name __pycache__ -exec rm -rf '{}' + ;


FROM python as app_base
RUN mkdir /app
WORKDIR /app
{{#dependencies_nf?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_nf}} {{_}}{{/dependencies_nf}}
{{/dependencies_nf?}}
{{#dependencies?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies}} {{_}}{{/dependencies}}
{{/dependencies?}}
COPY --from=requirements /requirements.nf/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements/ /python/versions/{{python.version}}/


FROM app_base as app_dev_base
{{#dependencies_nf_dev?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_nf_dev}} {{_}}{{/dependencies_nf_dev}}
{{/dependencies_nf_dev?}}
{{#dependencies_dev?}}
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install{{#dependencies_dev}} {{_}}{{/dependencies_dev}}
{{/dependencies_dev?}}
COPY --from=requirements /requirements.sys/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements.nf.dev/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements.dev/ /python/versions/{{python.version}}/


FROM app_dev_base as code
ENV PYTHONPATH="/app"
RUN passwd -d root
COPY .nf/.dir-locals.el /.dir-locals.el
RUN --mount=id=nfaptcache,target=/var/cache/apt,type=cache --mount=id=nfaptlib,target=/var/lib/apt,type=cache apt-get --no-install-recommends -y install openssh-server
COPY .nf/ssh_host_* /etc/ssh/
RUN mkdir -p /run/sshd
RUN chmod 0600 /etc/ssh/ssh_host_*
CMD ["/usr/sbin/sshd", "-o", "ListenAddress=0.0.0.0", "-o", "AllowTcpForwarding=yes", "-o", "UsePAM=no", "-o", "PasswordAuthentication=yes", "-o", "PermitEmptyPasswords=yes", "-o", "PermitRootLogin=yes", "-D"]


FROM app_dev_base as app_dev
CMD {{app_run_dev_command}}


{{#features.jupyter}}
FROM app_dev_base as jupyter
ENV PYTHONPATH="/app"
RUN mkdir /notebooks
WORKDIR /notebooks
CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--port=8888", "--LabApp.token="]


{{/features.jupyter}}
FROM app_base as app
COPY ./app /app/
RUN find /app -type d -name __pycache__ -exec rm -rf '{}' + ;
CMD {{app_run_command}}
