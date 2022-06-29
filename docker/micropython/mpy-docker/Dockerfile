FROM debian:stable-slim

RUN apt-get update && apt-get -y install build-essential libffi-dev pkg-config python3 python3-setuptools python3-dev git
WORKDIR /tmp/
RUN git clone https://github.com/micropython/micropython.git
WORKDIR /tmp/micropython/ports/unix
RUN make submodules
RUN make 

FROM debian:stable-slim
WORKDIR /root/
COPY --from=0 /tmp/micropython/ports/unix/micropython /usr/local/bin

