FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /service
COPY facade_service.py /service/facade_service.py
RUN pip install requests flask python-consul pika
EXPOSE 8000
CMD ["python", "-u", "facade_service.py"]
