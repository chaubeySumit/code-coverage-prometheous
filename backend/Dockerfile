FROM golang:1.23-alpine

WORKDIR /app

# Initialize module and fetch promhttp
RUN go mod init poc-backend && \
    go get github.com/prometheus/client_golang/prometheus/promhttp

COPY main.go ./

RUN go build -o server main.go

EXPOSE 8080

CMD ["./server"]
