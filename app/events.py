from flask_socketio import join_room, emit
from .extensions import socketio

@socketio.on("join")
def on_join(data):
    join_room(data["room"])
    emit("system", f'{data["user"]} joined #{data["room"]}', to=data["room"])

@socketio.on("message")
def on_message(data):
    body = data["body"][:500] # basic length limit
    emit("message", {"user": data["user"], "body": body}, to=data["room"])
