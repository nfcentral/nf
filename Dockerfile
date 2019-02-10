FROM alpine:3.9 as base
RUN apk add --no-cache dumb-init ca-certificates libc6-compat openssl readline libffi zlib bzip2 sqlite-dev
ENTRYPOINT ["/usr/bin/dumb-init"]


FROM base as python_build
RUN apk add --no-cache bash git build-base openssl-dev readline-dev libffi-dev zlib-dev bzip2-dev
RUN git clone --depth 1 https://github.com/pyenv/pyenv /python
ENV PYENV_ROOT=/python
RUN /python/bin/pyenv install 3.7.2
RUN find /python/versions/3.7.2 -depth \( \( -type d -a \( -name test -o -name tests \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \) -exec rm -rf '{}' + ;
ENV PATH="/python/versions/3.7.2/bin:${PATH}"


FROM base as python
COPY --from=python_build /python/versions/3.7.2 /python/versions/3.7.2
ENV PATH="/python/versions/3.7.2/bin:${PATH}"


FROM python_build as requirements
ENV PATH="/requirements.sys/bin:${PATH}"
ENV PYTHONPATH="/requirements.sys/lib/python3.7/site-packages"
RUN pip install --upgrade --prefix /requirements.sys pip setuptools
RUN find /requirements.sys -type d -name __pycache__ -exec rm -rf '{}' + ;

COPY requirements.txt /
ENV PATH="/requirements/bin:${PATH}"
ENV PYTHONPATH="/requirements/lib/python3.7/site-packages:${PYTHONPATH}"
RUN mkdir /requirements
RUN pip install --prefix /requirements -r requirements.txt
RUN find /requirements -type d -name __pycache__ -exec rm -rf '{}' + ;


FROM python as nf
RUN mkdir /nf
RUN mkdir /project
WORKDIR /project
ENV PYTHONPATH="/nf"
COPY --from=requirements /requirements.sys/ /python/versions/3.7.2/
COPY --from=requirements /requirements/ /python/versions/3.7.2/
COPY nf.py /nf/
COPY templates/ /nf/templates
ENTRYPOINT ["/usr/bin/dumb-init", "python", "/nf/nf.py"]
