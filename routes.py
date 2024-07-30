from app import app
from flask import render_template
from flask import request, jsonify
from models.log import LogModel


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mark_as_read', methods=['POST'])
def mark_as_read():
    try:
        data = request.json
        message_id = data.get('id')
        log = LogModel.objects.get(id=message_id)
        log.is_read = True
        log.save()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/delete_message', methods=['DELETE'])
def delete_message():
    try:
        data = request.json
        message_id = data.get('id')
        log = LogModel.objects.get(id=message_id)
        log.delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
