import requests
import flask
import uuid
import pika
import random
import consul
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

def forward_get():
    messag_url = random_message_url()
    logs_url = random_logging_url()

    print("...Sending GET to logging service...")
    uuid_make = {
            "uuid":str(uuid.uuid4()),
            "msg":flask.request.json.get('msg')
        }
    logs_response = requests.get(
        "{msg}/logging-service".format(msg=logs_url),
        json = uuid_make
    )
    print('1. Received response to GET from logging service:', logs_response.content)    

    msg_response = requests.get(
        "{msg}/messages".format(msg=messag_url),
        json = uuid_make
    )
    print('2. Received response to GET from message service:', msg_response.text)
    return msg_response.text

def forward_post():
    logs_url = random_logging_url()

    print("...Sending POST to logging service...")
    try:
        uuid_make = {
            "uuid":str(uuid.uuid4()),
            "msg":flask.request.json.get('msg')
        }
        logs_response = requests.post(
            "{msg}/logging-service".format(msg=logs_url),
           json = uuid_make
        )
        status = logs_response.status_code
        print('1. Received response to POST from logging service:', status)

        #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        queue = get_kv(consul_client, "queue")
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange='', routing_key=queue, body=flask.request.json.get('msg'))
        print(f" [x] Sent to message queue: %s"%flask.request.json.get('msg'))
        #connection.close()

        return app.response_class()

    except Exception as ex:
        raise ex
        flask.abort(400)

def register(consul_client, port):
    check_http = consul.Check.http(f'http://facade_service:{port}/health', interval='10s')
    consul_client.agent.service.register(
        'facade_service',
        service_id=f'facade_service',
        address="facade_service",
        port=port,
        check=check_http,
    ) 


def get_kv(c, name):  #retrieves a value from Consul's KV store and returns it as a string
    return c.kv.get(name)[1]['Value'].decode()[1:-1] #removing any surrounding quotation marks.


def discover_service(name):
    services = []
    while not services:
        for s in consul_client.health.service(name, passing=True)[1]:
            info = s['Service']
            services.append(f"{info['Address']}:{info['Port']}")
        if services:
            break
        time.sleep(2)
    return random.choice(services)


def random_logging_url():
    return f"http://{discover_service('logging_service')}/"
    #return f"http://{discover_service('logging_service')}/logging-service"


def random_message_url():
    return f"http://{discover_service('messages_service')}/messages-service"


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(status=200)

@app.route('/', methods=['GET','POST'])
def facade_serv():
    if flask.request.method == 'GET':
        return forward_get()
    elif flask.request.method == 'POST':
        return forward_post()
    else:
        flask.abort(405)

if __name__ == '__main__':
    port = 8000
    consul_client = consul.Consul(host="consul-server")
    register(consul_client, port)
    app.run(host="0.0.0.0",
            port=port,
            debug=True)
    connection.close()
