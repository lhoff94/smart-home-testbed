FROM koenkk/zigbee2mqtt

COPY data/configuration.yaml /app/data/configuration.yaml
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "/sbin/tini", "--", "node", "index.js"]
