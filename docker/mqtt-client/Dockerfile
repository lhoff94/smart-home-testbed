FROM python:3-slim
COPY entrypoint.sh mqtt-client.py /

ENTRYPOINT [ "/entrypoint.sh" ]

RUN apt update && apt install -y --no-install-recommends iproute2
RUN pip3 --no-cache-dir install paho-mqtt

CMD ["python3", "-u", "./mqtt-client.py"]