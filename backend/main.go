package main

import (
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// A standard HTTP request counter. Notice it does NOT track who the caller is.
var (
	httpRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests.",
		},
		[]string{"method", "uri", "status"},
	)
)

// Generic middleware just to tally requests
func metricsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Just incrementing with Method and URI
		httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, "200").Inc()
		next.ServeHTTP(w, r)
	})
}

func mockHandler(message string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(message))
	}
}

func main() {
	// Let's create two APIs: /api/users and /api/checkout
	http.Handle("/api/users", metricsMiddleware(mockHandler(`{"users": ["Alice", "Bob"]}`)))
	http.Handle("/api/checkout", metricsMiddleware(mockHandler(`{"status": "payment successful"}`)))

	// Expose the metrics endpoint for Prometheus
	http.Handle("/metrics", promhttp.Handler())

	log.Println("Go Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
