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
periodic_task_handler = TaskHandler()
periodic_task_handler.start_task_handler()


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


@app.route('/add-task', methods=['POST'])
def add_task():
    if request.is_json:
        received_data = request.get_json()
        task_id = db_ops.insert_new_task(received_data)

        if task_id is not None:
            task = {'task_id': task_id,
                    'scheduled_time': time.time(),
                    'period': int(received_data['taskFreq']),
                    'call': gcf_part_one,
                    }
            periodic_task_handler.insert_task(task)

    return 'Talk is cheap'


@app.route('/gcf-part-one', methods=['POST'])
def gcf_part_one(task_data):
    required_data = db_ops.get_data(task_data['task_id'], 'taskTargetURL', 'taskTargetId')
    print(required_data)


@app.route('/gcf-part-two', methods=['POST'])
def gcf_part_two():
    # get gcf's request for part two
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
