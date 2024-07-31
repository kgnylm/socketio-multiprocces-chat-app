import time
import threading
import socketio

HOST = 'http://localhost'
PORT = 5000

NUM_MESSAGES = 100
NUM_CLIENTS = 10


def send_messages(client_id):
    sio = socketio.Client()

    @sio.event
    def connect():
        print(f'Client {client_id} connected')

    @sio.event
    def disconnect():
        print(f'Client {client_id} disconnected')

    sio.connect(f'{HOST}:{PORT}')

    for i in range(NUM_MESSAGES):
        message_data = {
            'username': f'User{client_id}',
            'text': f'Message {i} from client {client_id}'
        }
        sio.emit('message', message_data)
        print(f'Client {client_id} sent: {message_data}')

        time.sleep(0.01)

    sio.disconnect()


if __name__ == '__main__':
    threads = []

    for i in range(NUM_CLIENTS):
        thread = threading.Thread(target=send_messages, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Tüm mesajlar gönderildi.")
