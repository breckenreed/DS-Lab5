import flask
import pika
import threading
import consul
import sys

msg = []
msg_lock = threading.Lock()

consul_client = consul.Consul(host="consul-server")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(status=200)

@app.route('/messages', methods=['GET'])


def message():
    global msg
    if len(msg) == 0:
        return "Insufficient messages count"
    with msg_lock:
        wiped_msg = msg.copy()
        msg.clear()    
    return ','.join(wiped_msg)
    
def queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    connection.start()
    channel = connection.channel()
    queue = get_key_value(consul_client, "queue")
    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        global msg
        with msg_lock:
            msg.append(body.decode())
        print(" [x] Received %r" % body.decode())
        print (','.join(msg))

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def get_key_value(c, name):
    return c.kv.get(name)[1]['Value'].decode()[1:-1]


def register(service_id, port):
    c = consul.Consul(host="consul-server")
    check_http = consul.Check.http(f"http://messages_service_{service_id}:{port}/health", interval='10s')
    c.agent.service.register(
        'messages_service',
        service_id=f"messages_service_{service_id}",
        address=f"messages_service_{service_id}",
        port=port,
        check=check_http)


if __name__ == '__main__':
    port = 8021
    service_id = int(sys.argv[1])
    register(service_id, port)
    queue_thread = threading.Thread(target = queue)
    queue_thread.start()
    app.run(host="0.0.0.0",
            port=port,
            debug=False)


# if __name__ == '__main__':
#     queue_thread = threading.Thread(target = queue)
#     queue_thread.start()
#     app.run(host='0.0.0.0', port='8021')
    
