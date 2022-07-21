FROM python:3
COPY mqtt-subscriber.py entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

RUN apt update && apt install -y --no-install-recommends iproute2

RUN pip3 --no-cache-dir install paho-mqtt

CMD ["python3", "-u","./mqtt-subscriber.py"]