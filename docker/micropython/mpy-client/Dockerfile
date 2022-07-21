FROM lhoff94/micropython-runtime:latest

RUN apt-get update && apt-get install iproute2 -y

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY new-mpy-payload /root/
CMD [ "micropython", "main.py" ]