FROM golang:1.23-alpine
WORKDIR /app
RUN go mod init poc-service && \
    go get github.com/prometheus/client_golang/prometheus/promhttp
COPY main.go ./
RUN go build -o server main.go
CMD ["./server"]
