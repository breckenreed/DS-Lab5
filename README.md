# DS-Lab5
Consul



Вимоги: <br />
Всі мікросервіси мають реєструватись при старті у Consul, кожного з сервісів може бути запущено декілька екземплярів: <br />
facade-service <br />
logging-service <br />
messages-service <br />

logging-service та messages-service було докеризовано у попередніх роботах. У цій роботі також докеризуємо facade-service аналогічним чином, але будемо запускати його в одиничному екземплярі. <br />
 
У рут-фолдері: <br />
```
docker-compose up hz1 hz2 hz3 consul-server consul-client rabbitmq
```
У терміналі контейнера consul-server: <br />

```
consul kv put hazelcast_addrs "hz1:5701,hz2:5701,hz3:5701"
consul kv put map "distributed_map"
consul kv put queue "LAB5-MQ"
consul kv put rabbit_host "rabbitmq"
```
<img width="501" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/fd7e99e4-4d23-4b46-820e-964be6272ab0"> <br />

<img width="715" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/8681f8e1-ce08-45c9-8d08-e9316bd96068"> <br />

Далі у рут-фолдері: <br />

```
docker-compose up --build facade_service logging_service_1 logging_service_2 logging_service_3 messages_service_1 messages_service_2 <br />
```


<img width="1434" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/377a8a7d-5f62-4ba3-97b8-ffd76f709268"> <br />

<img width="1036" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/2601194e-ad99-4900-bfeb-7a2789ffda84"> <br />

<img width="1120" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/654311f8-d806-46c1-adfe-ce6a391ac130"> <br />


<img width="718" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/ca8ee737-956c-46a7-8765-e4594c524d0f"> <br />



При звертанні facade-service до logging-service та messages-service, IP-адреси (і порти) мають зчитуватись facade-service з Consul. Не має бути задано в коді чи конфігураціях статичних значень адрес. <br />

``facade_service.py``: <br />

<img width="514" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/6b1936d0-3e14-4134-af77-459020adcadf"> <br />

``logging_service.py`` <br />

<img width="681" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/ab5abd68-5d6a-442c-a657-a99b7f7b9192"> <br />

``message_service.py`` <br />

<img width="561" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/5cca48d3-a5d6-4f5a-b2a5-9ae263f1dfe8"> <br />
<img width="690" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/68923503-85e0-4a7a-822f-2cf7eacf52f0"> <br />



Налаштування для клієнтів Hazelcast мають зберігатись як key/value у Consul і зчитуватись logging-service <br />
Налаштування для Message Queue (адреса, назва черги, …) мають зберігатись як key/value у Consul і зчитуватись facade-service та messages-service <br />

<img width="1173" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/ec4531c3-9a9e-4088-b2d5-df8a8a1e9c31"> <br />




