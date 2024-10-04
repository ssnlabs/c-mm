import threading
import time
import random

class LogicalClock:
    def __init__(self, pid):
        self.pid = pid  # Process ID
        self.clock = 0  # Logical clock value
        self.lock = threading.Lock()  # Lock for thread safety

    def increment_clock(self):
        """ Increment the clock for this process. """
        self.clock += 1

    def send_message(self, receiver):
        """ Send a message to another process with the current logical clock. """
        with self.lock:
            self.increment_clock()
            print(f"Process {self.pid} sending message with timestamp {self.clock} to Process {receiver.pid}")
        receiver.receive_message(self.clock)

    def receive_message(self, received_time):
        """ Update the logical clock on receiving a message. """
        with self.lock:
            self.clock = max(self.clock, received_time) + 1
            print(f"Process {self.pid} received message with timestamp {received_time}. Updated clock to {self.clock}")

    def perform_event(self):
        """ Simulate an internal event that increments the logical clock. """
        with self.lock:
            self.increment_clock()
            print(f"Process {self.pid} performs an internal event. Updated clock to {self.clock}")

    def run(self, peers):
        """ Simulate sending and receiving messages between processes. """
        for _ in range(5):
            # Perform an internal event
            self.perform_event()
            time.sleep(random.random())  # Random sleep to simulate concurrency
            
            receiver = random.choice(peers)  # Randomly pick a process to send a message to
            if receiver != self:  # Don't send to itself
                self.send_message(receiver)
            time.sleep(random.random())  # Random sleep to simulate concurrency


# Simulating logical clock across multiple processes using threading
def start_simulation():
    num_processes = 3
    processes = [LogicalClock(i) for i in range(1, num_processes + 1)]

    threads = []
    for process in processes:
        thread = threading.Thread(target=process.run, args=(processes,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

start_simulation()
