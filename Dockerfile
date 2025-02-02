FROM python:3.10-bullseye as build

COPY . .

RUN pip install poetry && \
    poetry build

FROM python:3.10-alpine

RUN apk add --no-cache ffmpeg

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=build dist/*.whl .
RUN pip install *.whl && rm -Rf *.whl

ENTRYPOINT ["earhorn"]
