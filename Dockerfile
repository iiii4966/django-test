FROM python:3.8.0-slim as builder

# TODO: version specification
RUN apt-get update \
        && apt-get install gcc -y \
        && apt-get clean

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -U -r requirements.txt

COPY . /usr/src/

# Latest

FROM python:3.8.0-slim

RUN apt-get update && apt-get install curl -y
RUN addgroup appgroup && adduser app

WORKDIR /home/app

COPY --from=builder /usr/src/project /home/app/
COPY --from=builder /usr/local/bin/ /usr/local/bin
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

USER app

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0", "--timeout=200", "project.wsgi"]

HEALTHCHECK  --interval=10s --timeout=3s \
                CMD curl http://0.0.0.0:8000/ || exit 1