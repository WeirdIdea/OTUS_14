HOST = '127.0.0.1'
PORT = 8080
DOCUMENT_ROOT = './html'
DEFAULT_FILE = 'index.html'

RESPONSE_CODE = { 200: 'HTTP/1.1 200 OK',
                  403: 'HTTP/1.1 403 Forbidden',
                  404: 'HTTP/1.1 404 Not Found',
                  405: 'HTTP/1.1 405 Method Not Allowed' }


# response = 'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
# content = 'Hello!'

