FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /service
COPY logging_service.py /service/logging_service.py
RUN pip install flask hazelcast-python-client python-consul
EXPOSE 8011
CMD ["python", "-u", "logging_service.py"]
