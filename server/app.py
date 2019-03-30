from flask import Flask, request
from flask_cors import CORS, cross_origin
import time
import json
from flask import jsonify
import subprocess
from tempfile import NamedTemporaryFile
from random import randint
from DatabaseOperations import DatabaseOperations
from TaskHandler import TaskHandler

app = Flask(__name__) #create the Flask app
CORS(app)

tmpDIR = './static/mirrors'
puppeteerDIR = '../puppeteer-jobs/generate-mirror.js'

db_ops = DatabaseOperations()
th = TaskHandler()
th.start_task_handler()

def func1():
    print('func #1')

def func2():
    print('func #2')


th.insert_task( {'name': 'task1', 'period': 15, 'scheduled_time':time.time()+10} )
th.insert_task( {'name': 'task2', 'period': 10, 'scheduled_time':time.time()+2} )
th.insert_task( {'name': 'task3', 'period': 30, 'scheduled_time':time.time()+10} )


@app.route('/generate-mirror', methods=['GET', 'POST'])
def generate_mirror():
    #time.sleep(randint(0, 3))   # for chaos
    data = request.data
    dataDict = json.loads(data)

    with NamedTemporaryFile(dir=tmpDIR) as tf:
        fname = tf.name + '.png'
        img = 'http://localhost:5000/static/mirrors/' + fname.rsplit('\\')[-1]
    print(fname, img, dataDict['url'])

    command = 'node {} {} {}'.format(puppeteerDIR, dataDict['url'], fname)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()
    p_status = proc.wait()

    # puppeteer job exited without error
    ret = {}
    if not err:
        jfname = fname.rsplit('.')[0] + '.json'
        with open(jfname) as f:
            data = json.load(f)
            ret[img] = data

    return jsonify(ret)


@app.route('/addTask', methods=['POST'])
def add_task():
    if request.is_json:
        received_data = request.get_json()
        db_ops.insert_new_task(received_data)
        # TODO: if insertion success, add this task as periodic cloud function

    return 'Talk is cheap'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
