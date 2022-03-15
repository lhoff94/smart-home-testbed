FROM python:3-slim

COPY entrypoint.sh test.py /

ENTRYPOINT ["/entrypoint.sh"]

RUN apt update && apt install -y --no-install-recommends iproute2

CMD ["python3", "-u", "./test.py"]
