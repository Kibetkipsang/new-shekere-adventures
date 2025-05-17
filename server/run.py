from app import create_app, socketio
from flask import Flask

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)

