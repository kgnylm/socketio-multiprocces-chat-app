from app import socketio, app
from flask_socketio import emit
from flask import request, jsonify
from models.log import LogModel
from queues import message_queue
import threading
import uuid

queue_lock = threading.Lock()


@socketio.on('connect')
def handle_connect():
    try:
        messages = LogModel.objects().order_by('created_at')
        for log in messages:
            data = {
                'id': str(log.id),
                'username': log.username,
                'message': log.message if log.type == "text" else "",
                'image': log.message if log.type == "image" else "",
                'is_read': log.is_read
            }
            if log.type == "image":
                emit('image', data)
            else:
                emit('message', data)
    except Exception as e:
        print(f"Error: {e}")


@socketio.on('message')
def handle_message(data):
    try:
        print(f'Received message: {data}')
        username = data.get('username', 'Anonymous')
        message_content = data.get('text', '').strip()

        with queue_lock:
            message_queue.put(('text', {'username': username, 'message': message_content}))
            print(f"Message queued: {message_queue}")
    except Exception as e:
        print(f"Error: {e}")


@socketio.on('image')
def handle_image(data):
    try:
        print('Received image data')
        image_data = data.get('image', '')

        user_agent = request.headers.get('User-Agent', 'unknown')
        username = f"Anon_{user_agent[:10]}_{uuid.uuid4().hex[:8]}"

        with queue_lock:
            message_queue.put(('image', {'username': username, 'image': image_data}))
            print(f"Image queued: {message_queue}")
    except Exception as e:
        print(f"Error: {e}")
