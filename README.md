# just 4 job interview
# Поиск ближайшего простого числа на микросервисах

1. Собираем RPC-сервер (можно пропустить, т.к. уже собран)
```
sudo apt-get install libpoco-dev
cd nearest_prime/server/build
cmake ..
make
```

2. Собираем мультиконтейнерное приложение
```
cd ../..
sudo docker-compose build
```

3. Запускаем
```
sudo docker-compose up
```

Для проверки (в data подставляем свое число):
curl --header "Content-Type: application/json" \
  --request POST \
  --data '10' \
  http://localhost:5000/prime/nearest
