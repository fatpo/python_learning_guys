import socket
import traceback


def handle_request(client):
    buf = client.recv(1024)
    print(buf)
    client.send(bytes("HTTP/1.1 200 OK\r\n\r\n", encoding='utf-8'))
    client.send(bytes("Hello, World", encoding='utf-8'))


def main():
    # socket 网络编程，一节课讲不清，自己课后学习
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 10005))
    sock.listen(5)

    while True:
        try:
            connection, address = sock.accept()

            handle_request(connection)

            connection.close()
        except Exception as ex:
            traceback.print_exc()
            print(ex)


if __name__ == '__main__':
    main()
