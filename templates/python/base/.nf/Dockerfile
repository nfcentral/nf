FROM alpine:3.9 as base
RUN apk add --no-cache dumb-init ca-certificates libc6-compat openssl readline libffi zlib bzip2 sqlite-dev
ENTRYPOINT ["/usr/bin/dumb-init"]


FROM base as python_build
RUN apk add --no-cache bash git build-base openssl-dev readline-dev libffi-dev zlib-dev bzip2-dev
RUN git clone --depth 1 https://github.com/pyenv/pyenv /python
ENV PYENV_ROOT=/python
RUN /python/bin/pyenv install {{python.version}}
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"
{{#features.freeze}}
ADD nf.pipfreeze /
{{/features.freeze}}
RUN apk add --no-cache rsync
COPY .nf/pipframer /bin
RUN chmod +x /bin/pipframer
RUN pipframer install --prefix /requirements.sys --upgrade pip setuptools wheel
ENV PATH="/requirements.sys/bin:${PATH}"
ENV PYTHONPATH="/requirements.sys/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN find /python/versions/{{python.version}} -depth \( \( -type d -a \( -name test -o -name tests -o -name __pycache__ \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \) -exec rm -rf '{}' + ;
RUN rm -rf /python/versions/{{python.version}}/lib/python{{python.version_shot}}/site-packages/*
RUN rm -rf /python/versions/lib/python{{python.version_short}}/ensurepip
RUN mv /python/versions/{{python.version}}/lib/libpython{{python.version_short}}m.a /
RUN rm -rf /python/versions/{{python.version}}/lib/python{{python.version_short}}/config-*

FROM base as python
COPY --from=python_build /python/versions/{{python.version}} /python/versions/{{python.version}}
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"


FROM python_build as requirements
RUN mv /libpython{{python.version_short}}m.a /python/versions/{{python.version}}/lib/

{{#dependencies_nf_build}}
RUN apk add --no-cache {{_}}
{{/dependencies_nf_build}}
COPY .nf/requirements.nf.txt /
ENV PATH="/requirements.nf/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf
RUN pipframer install --prefix /requirements.nf -r requirements.nf.txt
RUN find /requirements.nf -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_build}}
RUN apk add --no-cache {{_}}
{{/dependencies_build}}
COPY requirements.txt /
ENV PATH="/requirements/bin:${PATH}"
ENV PYTHONPATH="/requirements/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements
RUN pipframer install --prefix /requirements -r requirements.txt
RUN find /requirements -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_nf_dev_build}}
RUN apk add --no-cache {{_}}
{{/dependencies_nf_dev_build}}
COPY .nf/requirements.nf.dev.txt /
ENV PATH="/requirements.nf.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf.dev
RUN pipframer install --prefix /requirements.nf.dev -r requirements.nf.dev.txt
RUN find /requirements.nf.dev -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_dev_build}}
RUN apk add --no-cache {{_}}
{{/dependencies_dev_build}}
COPY requirements.dev.txt /
ENV PATH="/requirements.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.dev
RUN pipframer install --prefix /requirements.dev -r requirements.dev.txt
RUN find /requirements.dev -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#features.freeze}}
RUN pip freeze >/nf.pipfreeze
{{/features.freeze}}

FROM python as app_base
RUN mkdir /app
WORKDIR /app
{{#dependencies_nf}}
RUN apk add --no-cache {{_}}
{{/dependencies_nf}}
{{#dependencies}}
RUN apk add --no-cache {{_}}
{{/dependencies}}
COPY --from=requirements /requirements.nf/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements/ /python/versions/{{python.version}}/


FROM app_base as app_dev_base
{{#dependencies_nf_dev}}
RUN apk add --no-cache {{_}}
{{/dependencies_nf_dev}}
{{#dependencies_dev}}
RUN apk add --no-cache {{_}}
{{/dependencies_dev}}
COPY --from=requirements /requirements.nf.dev/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements.dev/ /python/versions/{{python.version}}/


FROM app_dev_base as code
ENV PYTHONPATH="/app"
COPY .nf/.dir-locals.el /.dir-locals.el
RUN apk add --no-cache openssh
COPY .nf/ssh_host_* /etc/ssh/
RUN chmod 0600 /etc/ssh/ssh_host_*
CMD ["/usr/sbin/sshd", "-o", "ListenAddress=0.0.0.0", "-o", "AllowTcpForwarding=yes", "-o", "PasswordAuthentication=yes", "-o", "PermitEmptyPasswords=yes", "-o", "PermitRootLogin=yes", "-D"]


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
