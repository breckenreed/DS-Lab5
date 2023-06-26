import flask
import hazelcast
import consul
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(status=200)

@app.route('/logging-service', methods=['GET', 'POST'])
def logging_serv():
    if flask.request.method == 'GET':
        return forward_get()
    else:
        return forward_post()

def forward_post():
    data=flask.request.json
    print('Logging received POST request from client: ', data)
    try:
        map.set(data["uuid"], data["msg"])
        print("Saved to hazelcast map")
        return "OK"
    except Exception as ex:
        raise ex
        print('Message cannot be saved to hazelcast map')
        return 500      

def forward_get():
    data=flask.request.json
    print('Logging received GET request from client: ', data)
    try:
        print('Return messages: ',  map.values())
        return ','.join(map.get_all(map.key_set()).values())
    except Exception as ex:
        raise ex
        return 400

def get_key_value(c, name):
    return c.kv.get(name)[1]['Value'].decode()[1:-1]

def register(consul_client, service_id, port):
    check_http = consul.Check.http(f'http://logging_service_{service_id}:{port}/health', interval='10s')
    consul_client.agent.service.register(
        'logging_service',
        service_id=f"logging_service_{service_id}",
        address=f"logging_service_{service_id}",
        port=port,
        check=check_http,)

if __name__ == '__main__':
    port = 8011
    service_id = int(sys.argv[1])
    consul_client = consul.Consul(host="consul-server")
    client = hazelcast.HazelcastClient(
        cluster_members=get_key_value(consul_client, "hazelcast_addrs").split(',')
    )
    m = get_key_value(consul_client, 'map')
    map = client.get_map(m).blocking()
    register(consul_client, service_id, port)
    app.run(host="0.0.0.0",
            port=port,
            debug=True)
