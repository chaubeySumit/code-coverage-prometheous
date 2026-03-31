package main

import (
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var httpRequestsTotal = promauto.NewCounterVec(
	prometheus.CounterOpts{
		Name: "http_requests_total",
		Help: "Total number of HTTP requests.",
	},
	[]string{"method", "uri", "status", "service"},
)

const serviceName = "user-service"

func metricsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, "200", serviceName).Inc()
		next.ServeHTTP(w, r)
	})
}

func mockHandler(msg string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(msg))
	}
}

func main() {
	http.Handle("/api/users",   metricsMiddleware(mockHandler(`{"users":["Alice","Bob"]}`)))
	http.Handle("/api/profile", metricsMiddleware(mockHandler(`{"profile":"Alice"}`)))
	http.Handle("/api/login",   metricsMiddleware(mockHandler(`{"token":"abc123"}`)))
	http.Handle("/metrics",     promhttp.Handler())

	log.Printf("%s running on :8081", serviceName)
	log.Fatal(http.ListenAndServe(":8081", nil))
}
