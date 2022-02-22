FROM python:slim
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

RUN pip3 install paho-mqtt

COPY ./curl.sh /curl.sh

CMD ["/mqtt-client.py"]