FROM python:3.10-slim
WORKDIR /qa
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY test_api.py .
CMD ["pytest", "-v", "test_api.py"]
