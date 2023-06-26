<img width="1226" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/0ac4a849-a543-48f3-9420-2167c3acca85"># DS-Lab5
Consul



Вимоги: <br />
Всі мікросервіси мають реєструватись при старті у Consul, кожного з сервісів може бути запущено декілька екземплярів: <br />
facade-service <br />
logging-service <br />
messages-service <br />

logging-service та messages-service було докеризовано у попередніх роботах. У цій роботі також докеризуємо facade-service аналогічним чином, щоб уся структура проекту працювала в одній підмережі докера і єдині звернення з локалхосту будуть йти на сам facade-service від curl. facade-service будемо запускати в одиничному екземплярі. <br />
 
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





Тестові повідомлення: надходять і до logging, і до message: <br />

<img width="1119" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/9faec198-504f-4833-a3ad-a22b1b503886"> <br />
<img width="1115" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/1e8dfa43-e0fb-4769-9c1d-9326a67cab10"> <br />
<img width="1134" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/815a46b7-2b9e-4e07-898f-614bc19df2a4"> <br />


Контейнер ``lab5-final-facade_service-1`` <br />
<img width="707" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/86b65aad-7d47-4878-99cc-dcbed5e8df86"> <br />

Контейнер ``lab5-final-logging_service_1-1``
<img width="1149" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/f952ec0d-8fdb-4ce6-b790-eb655d71930c"> <br />

Контейнер ``lab5-final-logging_service_2-1``
<img width="1157" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/1e7210ce-3a6c-4cd7-afd5-a6dacd7b5d0b"> <br />

Контейнер ``lab5-final-logging_service_3-1``
<img width="1170" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/e4ad4980-ae9c-4504-9528-e8802fe5ab4d"> <br />

Контейнер ``lab5-final-messages_service_1-1``
<img width="1224" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/01fd9f19-654d-4daa-b48e-f3e801ad182d"> <br />

Контейнер ``lab5-final-messages_service_2-1``
<img width="1226" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/22e948a2-fe21-405c-990f-57a0d9e5c185"> <br />


