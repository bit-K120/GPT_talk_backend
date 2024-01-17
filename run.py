from chatapp import create_app, socketio
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    socketio.run(app, port)
    # socketio.run(app, host='0.0.0.0', port=8000)
