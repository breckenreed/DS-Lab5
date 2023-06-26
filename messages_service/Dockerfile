FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /service
COPY message_service.py /service/message_service.py
RUN pip install flask pika python-consul
EXPOSE 8021
CMD ["python", "-u", "message_service.py"]
