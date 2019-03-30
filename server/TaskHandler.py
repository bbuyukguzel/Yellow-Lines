import threading
import time

class TaskHandler:
    def __init__(self):
        self._queue = []
        self.thread = threading.Thread(name='task_handler_thread', target=self.tick)
        self._is_queue_modified = False

    def insert_task(self, task_dict):
        self._queue.append(task_dict)
        self._is_queue_modified = True

    def start_task_handler(self):
        self.thread.start()

    def get_current_cycle_tasks(self):
        # keep list ordered
        if self._is_queue_modified:
            self._queue.sort(key=lambda x: x['scheduled_time'])
            self._is_queue_modified = False

        current_time = time.time()
        print(self._queue)
        for task in self._queue:
            if (task['scheduled_time'] <= current_time):
                yield task

    def tick(self):
        while True:
            for task in self.get_current_cycle_tasks():
                try:
                    print('\t', task['name'])
                    self._is_queue_modified = True
                    task['scheduled_time'] = task['scheduled_time'] + task['period']
                except StopIteration:
                    pass
            time.sleep(5)
