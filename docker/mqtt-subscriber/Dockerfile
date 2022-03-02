FROM python:3
COPY mqtt-subscriber.py entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

RUN pip3 --no-cache-dir install paho-mqtt

CMD ["python", "./mqtt-subscriber.py"]