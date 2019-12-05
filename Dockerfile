FROM alpine:3.10

RUN apk update && \
    apk add python3 py3-pip && \
    pip3 install flask flask_restplus pytest pexpect requests && \
    ln -s /usr/bin/python3 /usr/bin/python

COPY . /opt/mock-parser
WORKDIR /opt/mock-parser


EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]
