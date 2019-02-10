FROM alpine:3.9 as base
RUN apk add --no-cache dumb-init ca-certificates libc6-compat openssl readline libffi zlib bzip2 sqlite-dev
ENTRYPOINT ["/usr/bin/dumb-init"]


FROM base as python_build
RUN apk add --no-cache bash git build-base openssl-dev readline-dev libffi-dev zlib-dev bzip2-dev
RUN git clone --depth 1 https://github.com/pyenv/pyenv /python
ENV PYENV_ROOT=/python
RUN /python/bin/pyenv install {{python.version}}
RUN find /python/versions/{{python.version}} -depth \( \( -type d -a \( -name test -o -name tests \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \) -exec rm -rf '{}' + ;
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"


FROM base as python
COPY --from=python_build /python/versions/{{python.version}} /python/versions/{{python.version}}
ENV PATH="/python/versions/{{python.version}}/bin:${PATH}"


FROM python_build as requirements
ENV PATH="/requirements.sys/bin:${PATH}"
ENV PYTHONPATH="/requirements.sys/lib/python{{python.version_short}}/site-packages"
RUN pip install --upgrade --prefix /requirements.sys pip setuptools
RUN find /requirements.sys -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_nf_build}}
RUN apk add --no-cache {{_name}}
{{/dependencies_nf_build}}
COPY requirements.nf.txt /
ENV PATH="/requirements.nf/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf
RUN pip install --prefix /requirements.nf -r requirements.nf.txt
RUN find /requirements.nf -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_build}}
RUN apk add --no-cache {{_name}}
{{/dependencies_build}}
COPY requirements.txt /
ENV PATH="/requirements/bin:${PATH}"
ENV PYTHONPATH="/requirements/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements
RUN pip install --prefix /requirements -r requirements.txt
RUN find /requirements -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_nf_dev_build}}
RUN apk add --no-cache {{_name}}
{{/dependencies_nf_dev_build}}
COPY requirements.nf.dev.txt /
ENV PATH="/requirements.nf.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.nf.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.nf.dev
RUN pip install --prefix /requirements.nf.dev -r requirements.nf.dev.txt
RUN find /requirements.nf.dev -type d -name __pycache__ -exec rm -rf '{}' + ;

{{#dependencies_dev_build}}
RUN apk add --no-cache {{_name}}
{{/dependencies_dev_build}}
COPY requirements.dev.txt /
ENV PATH="/requirements.dev/bin:${PATH}"
ENV PYTHONPATH="/requirements.dev/lib/python{{python.version_short}}/site-packages:${PYTHONPATH}"
RUN mkdir /requirements.dev
RUN pip install --prefix /requirements.dev -r requirements.dev.txt
RUN find /requirements.dev -type d -name __pycache__ -exec rm -rf '{}' + ;


FROM python as app_base
RUN mkdir /app
WORKDIR /app
{{#dependencies}}
RUN apk add --no-cache {{_name}}
{{/dependencies}}
COPY --from=requirements /requirements.sys/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements.nf/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements/ /python/versions/{{python.version}}/


FROM app_base as app_dev_base
{{#dependencies_dev}}
RUN apk add --no-cache {{_name}}
{{/dependencies_dev}}
COPY --from=requirements /requirements.nf.dev/ /python/versions/{{python.version}}/
COPY --from=requirements /requirements.dev/ /python/versions/{{python.version}}/


FROM app_dev_base as code
ENV PYTHONPATH="/app"
RUN apk add --no-cache openssh
RUN ssh-keygen -A
CMD ["/usr/sbin/sshd", "-o", "ListenAddress=0.0.0.0", "-o", "AllowTcpForwarding=yes", "-o", "PasswordAuthentication=yes", "-o", "PermitEmptyPasswords=yes", "-o", "PermitRootLogin=yes", "-D"]


FROM app_dev_base as app_dev
{{#features.http_aiohttp}}
CMD ["gunicorn", "{{name}}:app", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.GunicornUVLoopWebWorker", "--workers", "1", "--reload"]
{{/features.http_aiohttp}}
{{#features.http_quart}}
CMD ["hypercorn", "-b", "0.0.0.0:8000", "--worker-class", "uvloop", "--workers", "1", "--reload", "{{name}}:app"]
{{/features.http_quart}}
{{#features.http_starlette}}
CMD ["hypercorn", "-b", "0.0.0.0:8000", "--worker-class", "uvloop", "--workers", "1", "--reload", "{{name}}:app"]
{{/features.http_starlette}}


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
{{#features.http_aiohttp}}
CMD ["gunicorn", "{{name}}:app", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.GunicornUVLoopWebWorker", "--workers", "1"]
{{/features.http_aiohttp}}
{{#features.http_quart}}
CMD ["uvicorn", "{{name}}::app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop", "--no-access-log"]
{{/features.http_quart}}
{{#features.http_starlette}}
CMD ["uvicorn", "{{name}}::app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop", "--no-access-log"]
{{/features.http_starlette}}
