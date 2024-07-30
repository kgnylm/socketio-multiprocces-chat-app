from queues import message_queue
from app import socketio, app
import threading
import multiprocessing
from models.log import LogModel

queue_lock = threading.Lock()


def message_handler():
    while True:
        with queue_lock:
            msg_type, data = message_queue.get()

        if data is None:
            break

        try:
            if msg_type == 'text':
                print(f'Processing message: {data}')
                username = data['username']
                message = data['message']

                with app.app_context():
                    log = LogModel(username=username, message=message, type="text")
                    log.save()

                socketio.emit('message',
                              {'id': str(log.id), 'username': username, 'message': message, 'is_read': log.is_read})

            elif msg_type == 'image':
                print('Processing image')
                username = data['username']
                image_base64 = data['image']

                with app.app_context():
                    log = LogModel(username=username, message=image_base64, type="image")
                    log.save()

                socketio.emit('image',
                              {'id': str(log.id), 'username': username, 'image': image_base64, 'is_read': log.is_read})

        except Exception as e:
            print(f"Error processing {msg_type}: {e}")
        finally:
            message_queue.task_done()


def start_workers():
    thread = threading.Thread(target=message_handler)
    thread.daemon = True
    thread.start()

    workers = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=message_handler)
        p.start()
        workers.append(p)
