import threading
import time


class TaskHandler:
    def __init__(self, min_period=5):
        self._queue = []
        self._thread = threading.Thread(name='Task Handler Thread', target=self.tick)
        self._is_queue_modified = False
        self._required_keys = {'name', 'scheduled_time', 'period'}
        self._min_period = min_period
        self._last_sorted_time = None

    def insert_task(self, task_dict):
        # validation of task_dict
        if self._required_keys <= task_dict.keys():
            self._queue.append(task_dict)
            self._is_queue_modified = True
        else:
            print('Task cannot be added to task queue {}'.format(task_dict))

    def start_task_handler(self):
        self._thread.start()

    def get_current_cycle_tasks(self):
        current_time = time.time()

        # keep list ordered if new task inserted or refresh time came. since executed tasks moved to
        # end of list and cannot be executed again before min_period sorting frequently is not necessary.
        if self._is_queue_modified or (self._last_sorted_time + self._min_period <= current_time):
            self._queue.sort(key=lambda x: x['scheduled_time'])
            self._is_queue_modified = False
            self._last_sorted_time = current_time

        for task in self._queue:
            if task['scheduled_time'] <= current_time:
                yield task

    def tick(self):
        while True:
            for task in self.get_current_cycle_tasks():
                try:
                    task['scheduled_time'] = task['scheduled_time'] + task['period']
                    self._queue.append(self._queue.pop(0))
                except StopIteration:
                    pass
            time.sleep(2)
