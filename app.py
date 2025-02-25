import os
import signal
from flask import Flask
from routes import order_bp
from extensions import WorkerSingleton
from database import db, db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.register_blueprint(order_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

def cleanup(signum):
    worker_pid = os.getpid()
    print(f"Worker {worker_pid} shutting down (signal {signum}). Cleaning up...")
    WorkerSingleton().wait_until_queue_empty()  # Wait until the queue is empty before shutting down
    WorkerSingleton().get_connection().close()
    print(f"Worker {worker_pid} cleanup complete.")
    exit(0)  # Exit gracefully

def setup_cleanup():
    signal.signal(signal.SIGTERM, cleanup)  # Handle SIGTERM (normal shutdown)
    signal.signal(signal.SIGINT, cleanup)   # Handle SIGINT (Ctrl+C)
    signal.signal(signal.SIGQUIT, cleanup)  # Handle SIGQUIT (usually Ctrl+\)

if __name__ == '__main__':
    setup_cleanup()  # Setup signal handlers
    app.run(debug=True)