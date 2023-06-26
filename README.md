# DS-Lab5
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

<img width="1165" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/dde8e61b-9856-47da-8bc4-1dd6a8fef740">


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

<img width="497" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/df4ec117-ed81-4cb9-97f9-855694a16edd"> <br />
<img width="331" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/95f71dd0-a2d6-45dc-8368-6a8df6bfe992"> <br />
<img width="403" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/6a5ee8f9-17eb-4efa-958c-e3d457dd2638"> <br />

``logging_service.py`` <br />
<img width="606" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/948202da-e238-4993-a35e-13bd6206ccf3">

``message_service.py`` <br />
<img width="722" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/3f34a06a-f8cb-42c8-bf46-de8d404acbd1">


Налаштування для клієнтів Hazelcast мають зберігатись як key/value у Consul і зчитуватись logging-service <br />
Налаштування для Message Queue (адреса, назва черги, …) мають зберігатись як key/value у Consul і зчитуватись facade-service та messages-service <br />

<img width="1173" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/ec4531c3-9a9e-4088-b2d5-df8a8a1e9c31"> <br />



Тестові повідомлення: надходять і до logging, і до message: <br />
<img width="1021" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/f7207b3a-bc79-4c1d-86a9-a03db1a188ab"> <br />
<img width="1028" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/a186c57c-9f9d-4671-82a2-8372c3aa36f6"> <br />

Та повертаються з обох мікросервісів через GET <br />
<img width="1143" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/3405e12f-2ed5-4406-aa2b-6eb554664966"> <br />





Контейнер ``lab5-final-facade_service-1`` <br />
<img width="879" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/d4dc0d82-21fa-423c-a1e3-b704fa853733">  <br />
<img width="1387" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/a4871122-b80b-42af-9b28-3efc918bd9c6">  <br />


Контейнер ``lab5-final-logging_service_1-1``  <br />
<img width="1385" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/e9fe9cee-1fd6-4107-81dd-645d6bfc7972"> <br />

Контейнер ``lab5-final-logging_service_2-1``
<img width="878" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/89ac45bf-6829-45ec-824a-43b5ebb2b8ef"> <br />

Контейнер ``lab5-final-logging_service_3-1``
<img width="856" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/a058c165-82c9-4b2d-bd21-95842afe858e"> <br />

Контейнер ``lab5-final-messages_service_1-1``
<img width="789" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/09983f56-1f0e-41c2-85f3-b4393eec82c3"> <br />

Контейнер ``lab5-final-messages_service_2-1``
<img width="916" alt="image" src="https://github.com/breckenreed/DS-Lab5/assets/62158298/bb7d319c-1bd4-4ae3-a68d-62cd7dd148fc"> <br />


