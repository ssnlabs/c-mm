import threading
import time
import random

class VectorClock:
    def __init__(self, pid, num_processes):
        self.pid = pid  # Process ID
        self.clock = [0] * num_processes  # Vector clock
        self.num_processes = num_processes
        self.lock = threading.Lock()  # Lock for thread safety

    def increment_clock(self):
        """ Increment the clock for this process. """
        self.clock[self.pid] += 1

    def send_message(self, receiver, message):
        """ Send a message to another process with the current vector clock. """
        with self.lock:
            self.increment_clock()
            print(f"Process {self.pid} sending message '{message}' with clock {self.clock} to Process {receiver.pid}")
        receiver.receive_message(message, self.clock.copy())

    def receive_message(self, message, sender_clock):
        """ Update the vector clock on receiving a message. """
        with self.lock:
            # Element-wise max between the current clock and the received clock
            for i in range(self.num_processes):
                self.clock[i] = max(self.clock[i], sender_clock[i])
            self.increment_clock()  # Increment own clock after receiving the message
            print(f"Process {self.pid} received message '{message}' with sender's clock {sender_clock}. Updated clock to {self.clock}")

    def perform_event(self):
        """ Simulate an internal event that increments the vector clock. """
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
                self.send_message(receiver, f"Message from Process {self.pid}")
            time.sleep(random.random())  # Random sleep to simulate concurrency


# Simulating vector clock across multiple processes using threading
def start_simulation():
    num_processes = 3
    processes = [VectorClock(i, num_processes) for i in range(num_processes)]

    threads = []
    for process in processes:
        thread = threading.Thread(target=process.run, args=(processes,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

start_simulation()
