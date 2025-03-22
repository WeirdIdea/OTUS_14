import socket
import logging
from dataclasses import replace

import const_values
import os


def get_head(code):
    return f'{const_values.RESPONSE_CODE[code]}\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'


def get_content(path):
    with open(path) as file:
        return get_head(200) + file.read()


def get_response(url: str) -> str:
    url = url.replace('%20', ' ')
    if url == '/':
        # default - index.html
        path = os.path.join(const_values.DOCUMENT_ROOT, const_values.DEFAULT_FILE)
    else:
        path = os.path.normpath(os.path.join(const_values.DOCUMENT_ROOT, url[1:]))
    logging.info(f'File requested: {path}')
    if os.path.isfile(path):
        with open(path) as file:
            return get_content(path)
    elif os.path.isdir(path):
        path = os.path.normpath(os.path.join(path, const_values.DEFAULT_FILE))
        if os.path.isfile(path):
            return get_content(path)
        else:
            return get_head(404)
    else:
        return get_head(404)


def try_answer(method: str, url: str) -> str:
    if method == 'HEAD':
        logging.info('Method of Request is HEAD')
        return get_head(200)
    elif method == 'GET':
        logging.info('Method of Request is GET')
        return get_response(url)
    else:
        logging.info('Method of Request is not allowed')
        return get_head(405)


def handle_request(req: str):
    req_text = req.split('\n')
    if req_text[0].count(' ') == 2:
        # first line of request is correct and not empty
        method, url, protocol = req_text[0].split(' ')
        return try_answer(method, url)
    else:
        logging.error(f'Request is empty')


def start_server():
    try:
        server.bind((const_values.HOST, const_values.PORT))
        server.listen()
    except socket.error as e:
        logging.error('Server startup error')
    logging.info('Server is started!')
    while True:
        client_socket, add = server.accept()
        try:
            request = client_socket.recv(1024).decode('utf-8')
            logging.info(f'Request:\n{request}')
            client_socket.send(handle_request(request).encode('utf-8'))
            client_socket.shutdown(socket.SHUT_WR)
        except Exception as e:
            logging.error(f'Invalid request: {e}')
        finally:
            try:
                client_socket.close()
            except Exception as e:
                logging.error(f'Error shutdown connection: {e}')


logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
start_server()