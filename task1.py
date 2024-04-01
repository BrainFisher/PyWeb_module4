import os
import json
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Функція для обробки запитів HTTP


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Метод обробки GET-запиту
    def do_GET(self):
        # Розбираємо URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Встановлюємо код відповіді 200 (OK)
        self.send_response(200)

        # Встановлюємо заголовок Content-type
        if path.endswith('.html'):
            self.send_header('Content-type', 'text/html')
        elif path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
        elif path.endswith('.png'):
            self.send_header('Content-type', 'image/png')

        # Завершуємо заголовки
        self.end_headers()

        # Відкриваємо файл та відправляємо його відповідь
        with open(f'C:\\Users\\User\\Desktop\\My_repo\\PyWeb_module4\\front-init{path}', 'rb') as f:
            self.wfile.write(f.read())

    # Метод обробки POST-запиту
    def do_POST(self):
        # Отримуємо довжину POST-даних
        content_length = int(self.headers['Content-Length'])
        # Отримуємо POST-дані
        post_data = self.rfile.read(content_length)
        # Розбираємо POST-дані
        post_data = parse_qs(post_data.decode('utf-8'))

        # Перетворюємо час в формат рядка
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Зберігаємо дані у JSON файл
        with open('storage/data.json', 'a') as file:
            json.dump({current_time: post_data}, file)
            file.write('\n')

        # Встановлюємо код відповіді 200 (OK)
        self.send_response(200)
        # Встановлюємо заголовок Content-type
        self.send_header('Content-type', 'text/plain')
        # Завершуємо заголовки
        self.end_headers()
        # Відправляємо повідомлення про успішне збереження даних
        self.wfile.write(b'Data successfully saved to storage/data.json')


# Клас HTTP сервера з підтримкою потоків
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


# Функція, яка виконує HTTP сервер
def run_http_server():
    # Створюємо екземпляр HTTP сервера з адресою localhost і портом 3000
    httpd = ThreadedHTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
    # Запускаємо HTTP сервер
    httpd.serve_forever()


# Функція, яка виконує Socket сервер
def run_socket_server():
    # Створюємо UDP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Прив'язуємо сокет до адреси і порту
        server_socket.bind(('localhost', 5000))
        print('Socket server started at port 5000')
        while True:
            # Отримуємо дані
            data, addr = server_socket.recvfrom(1024)
            # Друкуємо отримані дані
            print(f'Received message: {data.decode("utf-8")} from {addr}')


# Запускаємо HTTP сервер у окремому потоці
http_thread = threading.Thread(target=run_http_server)
http_thread.start()

# Запускаємо Socket сервер
run_socket_server()
