#!/bin/sh
# Generate traffic to the backend so Prometheus knows the APIs exist

while true; do
  curl -s http://go-backend:8080/api/users > /dev/null
  curl -s http://go-backend:8080/api/checkout > /dev/null
  sleep 2
done
