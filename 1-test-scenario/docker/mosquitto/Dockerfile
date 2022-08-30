FROM eclipse-mosquitto:latest

COPY entrypoint.sh mosquitto.conf /
EXPOSE 1883
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto.conf"]
