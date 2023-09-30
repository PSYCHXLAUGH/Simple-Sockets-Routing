# Задача

- Прочитать запрос и выяснить что пользователь хочет сделать
- Какие методы пользователь использует и на какую страницу направляется

#### Реализация следующих функций

- обработка запросов от пользователя
- маршрутизация запросов (routing)


# Теория

Работать мы будем с протоколом **http** который базируется на протоколах
<br>
```http``` - находится выше протокола tcp
- tcp - находится выше протокола ip
- ip - протокол с самым низким уровнем абстракции

Особеность протокола ip в том, что между двумя хостами создается тоннель передачи данных
###Пакеты могут
- Дублироваться 
- Потеряться
- Повредиться
- Прийти в неправильном порядке

Основная часть протокола IP - ip address. Поскольку протокол IP был не слишком надежным
то был разработан транспортный протокол TCP - Transmission Control Protocol — протокол управления передачей
который превносит порядок в передачу данных по протоколу IP. Протокол TCP следит за порядком получения и отправки
пакетов. Если пакетов не хватает он делает повторный запрос отправителю, если пришли дубли - он их убирает.
Его особенность в том, что он превносит в эту конструкцию передачи данных **port**. Порты нужны для того, чтобы 
несколько приложений могли использовать TCP и при этом не занимали собой весь тоннель. 

#### Socket
socket - пара **ip**:**port**

- Клиентские сокеты
- Серверные сокеты

#### Установка соединения между двумя хостами

- socket.AF_INET - сокращение от adress family. INET - сам протокол IP который бывает двух верский ipv4, ipv6. AF_INET это
4 версия, если нам нужна 6 версия то INET6. 
- socket.SOCK_STREAM - это тип сокета для TCP и протокол, который будет использоваться для передачи сообщений в сети


```python
import socket

URLS = {
    '/': 'hello index',
    '/route': 'hello route',
}


def parse_request(request):
    parsed = request.split(' ')
    print(parsed)
    method = parsed[0]
    url = parsed[1]
    print(method, url)
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 method is not allowed\n\n', 405
    if url not in URLS:
        return 'HTTP/1.1 404 page not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200


def generate_payload(code, url):
    if code == 404:
        return f'<h1>error {code} not found</h1>'.encode('utf-8')
    if code == 405:
        return f'<h1>error {code} method not allowed</h1>'.encode('utf-8')
    return f'<h1> {URLS[url]}</h1>'.encode('utf-8')

test

def generate_response(request):
    method, url = parse_request(request)
    # Ответ будет состоять из двух частей
    # Заголовок
    headers, code = generate_headers(method, url)
    # Полезная нагрузка (тело ответа)
    payload = generate_payload(code, url)

    return headers.encode('utf-8') + payload


def main():
    # Создаем судъект того, кто будет принимать запрос
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # связывание субъекта с конкретным адресом и портом
    server.bind(
        ('localhost', 4444)  # теперь сокет ждет обращение по этому адресу и конкретному порту
    )
    # начинаем прослушивать порт
    server.listen()

    # взаимодействие между клиентом и сервером не единоразовый процесс
    # мы будем использовать бесконечный цикл

    while True:
        # серверный сокет получил ответ
        client_socket, client_addr = server.accept()
        # получаем запрос от клиента
        request = client_socket.recv(1024)

        response = generate_response(request.decode('utf-8'))

        # socket's понимают только bytes
        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':  # Проверка на самостоятельный файл.
    main()
```