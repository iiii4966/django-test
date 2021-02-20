FROM python:3.8.0-slim as builder

RUN apt-get update \
        && apt-get install gcc -y \
        && apt-get clean

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -U -r requirements.txt

COPY . /usr/src/

# Latest

FROM python:3.8.0-slim

RUN addgroup appgroup && adduser app

WORKDIR /home/app

COPY --from=builder /usr/src/project /home/app/
COPY --from=builder /usr/local/bin/ /usr/local/bin
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

USER app

CMD ["gunicorn", "--bind=0.0.0.0", "--timeout=200", "project.wsgi"]

EXPOSE 8000