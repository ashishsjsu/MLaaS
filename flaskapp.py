from __future__ import absolute_import
from celery import Celery
import os
import random
import time
from datetime import datetime
from flask import Flask, request, session, flash, redirect, url_for, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

celery = Celery(app.name)
#confidure celery from a config file
celery.config_from_object('celeryconfig')

#define elasticsearch host and port
ES_HOST = {
	"host": "localhost",
	"port": 9200
}

#create elasticsearch object
es = Elasticsearch(hosts = [ES_HOST])


@celery.task(bind=True)
def spark_job_task(self):
	
	task_id = self.request.id
	master_path = 'local[2]'
	project_dir  = "/home/ken/Desktop/"
	spark_code_path = project_dir + "wordcount.py"
	
	result = os.system("/usr/local/spark-1.4.0-bin-hadoop2.6/bin/spark-submit --master %s %s %s" % (master_path, spark_code_path,  self.request.id))

	return {'current' : 100, 'total' : 100, 'status' : 'Task Completed!', 'result': 10, 'result': result}


#define routes for the server
@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':
		return "Hello World!"

@app.route('/sparktask', methods=["POST"])
def sparktask():
	
	task = spark_job_task.apply_async()
	#create an index in elasticsearch to store the sparkmjob info
	if not es.indices.exists('spark-jobs'):
		print ("Creating index - '%s'" % 'spark-jobs')
		res = es.indices.create(index="spark-jobs", body={
				"settings": {
					"number_of_shards": 1,
					"number_of_replicas": 0
				}
			})
		print res

	#create a new doc for the above index
	es.index(index="spark-jobs", doc_type="job", id=task.id, body={
			"current" : 0,
			"total": 100,
			"status": "Spark job pending...",
			"start_time": datetime.utcnow()
		})

	return jsonify({'task_id': task.id}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
	    
    task = spark_job_task.AsyncResult(task_id)

    if task.state == "FAILURE":
    	response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info)
    	}
    else:
    	es_task_info = es.get(index = "spark-jobs", doc_type="job", id=task_id)	
    	response = es_task_info['_source']
    	response['state'] = task.state

    return jsonify(response)


if __name__== '__main__':
	app.run(debug=True)
