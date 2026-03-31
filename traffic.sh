#!/bin/sh
# Simulates real users hitting all 3 microservices

while true; do
  # user-service traffic
  curl -s http://user-service:8081/api/users    > /dev/null
  curl -s http://user-service:8081/api/profile  > /dev/null
  curl -s http://user-service:8081/api/login    > /dev/null
  curl -s http://user-service:8081/api/settings > /dev/null

  # checkout-service traffic
  curl -s http://checkout-service:8082/api/checkout > /dev/null
  curl -s http://checkout-service:8082/api/payment  > /dev/null
  curl -s http://checkout-service:8082/api/orders   > /dev/null

  # inventory-service traffic
  curl -s http://inventory-service:8083/api/products   > /dev/null
  curl -s http://inventory-service:8083/api/stock      > /dev/null
  curl -s http://inventory-service:8083/api/categories > /dev/null

  sleep 2
done
