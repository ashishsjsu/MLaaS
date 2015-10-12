from __future__ import absolute_import
from celery import Celery
import os
import random
import time
from datetime import datetime
from flask import Flask, request, session, flash, redirect, url_for, jsonify

app = Flask(__name__)

celery = Celery(app.name)
celery.config_from_object('celeryconfig')

@celery.task
def spark_job_task(self):
	
	task_id = self.request.id
	master_path = 'local[2]'
	project_dir  = "/home/ken/Desktop/"
	spark_code_path = project_dir + "wordcount.py"
	
	os.system("/usr/local/spark-1.4.0-bin-hadoop2.6/bin/spark-submit --master %s %s %s" % (master_path, spark_code_path, self.request.id))

	return {'current' : 100, 'total' : 100, 'status' : 'Task Completed!', 'result': 10}

	
@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':
		return "Hello World!"

@app.route('/sparktask', methods="POST")
def sparktask():
	
	task = spark_job_task.apply_async()
	
	return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

if __name__== '__main__':
	app.run(debug=True)
