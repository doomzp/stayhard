from multiprocessing import Process, Event, Queue
import time

def worker(pause_event, stop_event, output_queue):
    while not stop_event.is_set():
        if not pause_event.is_set():
            # Do some work here
            output_queue.put("Working")
        time.sleep(1)

def main():
    pause_event = Event()
    stop_event = Event()
    output_queue = Queue()
    p = Process(target=worker, args=(pause_event, stop_event, output_queue))
    p.start()

    while True:
        # Do some work in the main process here
        time.sleep(1)

        # Pause the worker process
        pause_event.set()

        # Wait for the worker to finish processing any pending work
        while not output_queue.empty():
            print(output_queue.get())

        # Stop the worker process
        stop_event.set()

        # Wait for the worker to exit
        p.join()

        # Restart the worker process
        pause_event.clear()
        stop_event.clear()
        output_queue = Queue()
        p = Process(target=worker, args=(pause_event, stop_event, output_queue))
        p.start()

if __name__ == '__main__':
    main()
