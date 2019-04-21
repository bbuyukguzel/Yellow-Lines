import threading
import time
import datetime
from DatabaseOperations import DatabaseOperations


class TaskHandler:
    def __init__(self, thread_name, function, period):
        self._period = period
        self._thread = threading.Thread(name=thread_name, target=self.tick)
        self._tasks = []
        self._function = function
        self._cycle_started = 0
        self._db_ops = DatabaseOperations()

    def start_task_handler(self):
        self._thread.start()

    def get_current_cycle_tasks(self):
        self._tasks = self._db_ops.get_tasks()

    def run_task(self, task):
        # run task here
        new_next_execution = task['nextExecution'] + datetime.timedelta(seconds=task['taskFreq'])
        self._db_ops.update_task(task['_id'], 'nextExecution', new_next_execution)

    def tick(self):
        while True:
            current_task = None
            current_time = time.time()

            # refresh current cycle tasks
            if current_time - self._cycle_started >= self._period:
                self.get_current_cycle_tasks()
                self._cycle_started = current_time

            while self._tasks:
                if current_task is None:
                    current_task = self._tasks.pop(0)                   # get first task
                if current_task['nextExecution'] <= datetime.datetime.utcnow():        # if execution time came
                    self.run_task(current_task)
                    current_task = None                                 # remove executed task from list
                time.sleep(1)
            time.sleep(5)
