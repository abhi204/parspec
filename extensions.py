import threading
import queue
import os
import time
from database import db_driver

# Each worker process will have its own instance of this class and its own message queue and processor thread
class WorkerSingleton:
    _instances = {}  # Worker-local storage

    def __new__(cls):
        worker_id = os.getpid()
        if worker_id not in cls._instances:
            cls._instances[worker_id] = super().__new__(cls)
            cls._instances[worker_id]._initialized = False
        return cls._instances[worker_id]

    def __init__(self):
        if not getattr(self, "_initialized", False):
            self.queue = queue.Queue()
            self._stop_event = threading.Event()
            self.processor_thread = threading.Thread(
                target=process_messages, args=(self.queue, self._stop_event)
            )
            self.processor_thread.daemon = True
            self.processor_thread.start()
            self._initialized = True

    def getQ(self):
        return self.queue

    def stop(self):
        self._stop_event.set()
        self.processor_thread.join()

    def wait_until_queue_empty(self):
        self.queue.join()  # Blocks until all items in the queue have been processed
        self.stop()

def process_messages(message_queue, stop_event):
    while not stop_event.is_set() or not message_queue.empty():
        cursor = db_driver.cursor()
        try:
            order_id = message_queue.get(timeout=1)  # Non-blocking get with timeout
            print(f"Recieved id: {order_id}")
            cursor.execute(f"UPDATE orders SET status='PROCESSING', started_at=NOW() WHERE id={order_id}")
            db_driver.commit()
            print(f"processing id: {order_id}")

            time.sleep(5) # Simulate processing time

            cursor.execute(f"UPDATE orders SET status='COMPLETED', completed_at=NOW() WHERE id={order_id}")
            db_driver.commit()
            print(f"completed id: {order_id}")

            # Process the message
            message_queue.task_done()  # Indicate that a formerly enqueued task is complete
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            print("Message processor shutting down")
            break
    print("Processor thread has been stopped.")
