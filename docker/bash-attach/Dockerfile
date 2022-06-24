FROM python:3-slim

COPY entrypoint.sh test.py /

ENTRYPOINT ["/entrypoint.sh"]

RUN apt update && apt install -y --no-install-recommends iproute2

RUN apt install -y --no-install-recommends python3-pip iputils-ping

RUN pip3 install paho-mqtt

CMD ["python3", "-u", "./test.py"]
