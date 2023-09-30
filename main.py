import socket

URLS = {
    '/': 'hello index',
    '/route': 'hello route',
}


def test():
    pass

def parse_request(request):
    parsed = request.split(' ')
    print(parsed)
    method = parsed[0]
    url = parsed[1]
    print(method, url)
    return method, url

def musr():
    return

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
