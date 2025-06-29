FROM golang:1.24-alpine

WORKDIR /app

COPY . .

RUN go get github.com/gorilla/websocket
RUN go build -o main .

EXPOSE 8095

CMD ["./main"]
