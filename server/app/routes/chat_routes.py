from flask_socketio import emit, join_room
from . import socketio

@socketio.on('join')
def on_join(data):
    room = data['trip_id']
    join_room(room)
    emit('status', {'msg': f"{data['username']} joined the trip chat."}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['trip_id']
    emit('message', data, room=room)
