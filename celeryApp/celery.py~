from __future__ import absolute_import
from celery import Celery

celeryObj = Celery('celeryApp', include=['celeryApp.flaskapp'])
celeryObj.config_from_object('celeryconfig')

if __name__ == "__main__":
	celeryObj.start()
